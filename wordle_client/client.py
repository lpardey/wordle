import json
import logging
from typing import Type, TypeVar
import requests
from requests import Response

from wordle_schemas.game import (
    BasicResponse,
    BasicStatus,
    GameConfig,
    GameCreationResponse,
    GameStatusResponse,
    TakeAGuessRequest,
    TakeAGuessResponse,
)

GenericResponse = TypeVar("GenericResponse", bound=BasicResponse)

logger = logging.getLogger("WordleGame")


class WordleClientException(Exception):
    pass


class WordleClient:
    def __init__(self, service_url="http://localhost:8000") -> None:
        self.service_url = service_url

    def check_http_status(self, response: Response) -> None:
        if not response.status_code < 400:
            message = f"Error contacting service ({self.service_url}): [{response.status_code}] - {response.reason}"
            raise WordleClientException(message)

    def check_response_status(self, response: BasicResponse) -> None:
        if response.status != BasicStatus.OK:
            message = f"Error processing request: {response.message}"
            raise WordleClientException(message)

    def process_response(self, response: Response, response_type: Type[GenericResponse]) -> GenericResponse:
        self.check_http_status(response)
        parsed_response = response_type(**json.loads(response.text))
        self.check_response_status(parsed_response)
        return parsed_response

    def create_game(self, game_config: GameConfig) -> GameCreationResponse:
        url = f"{self.service_url}/game"
        response = requests.post(url=url, json=game_config.dict())
        parsed_response = self.process_response(response=response, response_type=GameCreationResponse)
        return parsed_response

    def get_game_status(self, game_id: int) -> GameStatusResponse:
        url = f"{self.service_url}/game/{game_id}"
        response = requests.get(url=url)
        parsed_response = self.process_response(response=response, response_type=GameStatusResponse)
        return parsed_response

    def take_a_guess(self, game_id: int, guess_request: TakeAGuessRequest) -> TakeAGuessResponse:
        url = f"{self.service_url}/game/{game_id}"
        response = requests.post(url=url, json=guess_request.dict())
        parsed_response = self.process_response(response=response, response_type=TakeAGuessResponse)
        return parsed_response

    def health_check(self) -> BasicResponse:
        url = f"{self.service_url}/healthcheck"
        response = requests.get(url)
        parsed_response = self.process_response(response, BasicResponse)
        return parsed_response

    def get_health_check(self) -> bool:
        try:
            response = self.health_check()
            return (response.status == BasicStatus.OK) and (response.message == "Wordle is OK")

        except Exception as e:
            logger.exception(e)
            return False
