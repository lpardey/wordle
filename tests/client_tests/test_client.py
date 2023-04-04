import json
from typing import Type
import pytest
from requests import Response
from wordle_client.client import GenericResponse, WordleClient, WordleClientException
from wordle_schemas.game import BasicResponse, BasicStatus
from unittest import mock


@pytest.mark.parametrize(
    "status_code, reason, check_http_status_side_effect",
    [
        pytest.param(
            404,
            "Not Found",
            WordleClientException("Error contacting service (http://localhost:8000): [404] - Not Found"),
            id="HTTP error 404",
        ),
        pytest.param(
            500,
            "Internal Server Error",
            WordleClientException("Error contacting service (http://localhost:8000): [500] - Internal Server Error"),
            id="HTTP error 500",
        ),
    ],
)
def test_check_http_status_client_or_server_error(
    status_code: int,
    reason: str,
    check_http_status_side_effect: WordleClientException | None,
    basic_wordle_client: WordleClient,
):
    response = Response
    response.status_code = status_code
    response.reason = reason
    expected_message = str(check_http_status_side_effect)

    with pytest.raises(WordleClientException) as exc_info:
        basic_wordle_client.check_http_status(response=response)

    assert str(exc_info.value) == expected_message


@pytest.mark.parametrize(
    "status_code, reason, expected_result",
    [
        pytest.param(
            200,
            "OK",
            None,
            id="HTTP not client or server error 200",
        ),
        pytest.param(
            307,
            "Temporary Redirect",
            None,
            id="HTTP not client or server error 307",
        ),
    ],
)
def test_check_http_status_not_client_or_server_error(
    status_code: int,
    reason: str,
    expected_result: None,
    basic_wordle_client: WordleClient,
):
    response = Response
    response.status_code = status_code
    response.reason = reason

    result = basic_wordle_client.check_http_status(response=response)

    assert result == expected_result


def test_check_response_status_failure(basic_wordle_client: WordleClient):
    response = BasicResponse(status=BasicStatus.ERROR, message="Take a guess")
    expected_message = str(WordleClientException(f"Error processing request: {response.message}"))

    with pytest.raises(WordleClientException) as exc_info:
        basic_wordle_client.check_response_status(response=response)

    assert (str(exc_info.value)) == expected_message


def test_check_response_status_success(basic_wordle_client: WordleClient):
    response = BasicResponse(status=BasicStatus.OK, message="Take a guess")
    expected_result = None

    result = basic_wordle_client.check_response_status(response=response)

    assert result == expected_result


@pytest.mark.parametrize(
    "status_code, reason, check_http_status_side_effect, response_type, check_response_status_side_effect",
    [
        pytest.param(
            404,
            "Not Found",
            WordleClientException("Error contacting service (http://localhost:8000): [404] - Not Found"),
            BasicResponse,
            None,
            id="HTTP status failure",
        ),
        pytest.param(
            200,
            "OK",
            None,
            BasicResponse,
            WordleClientException("Error processing request: Take a guess"),
            id="Response status failure",
        ),
    ],
)
def test_process_response_failure(
    status_code: int,
    reason: str,
    check_http_status_side_effect: WordleClientException | None,
    response_type: Type[GenericResponse],
    check_response_status_side_effect: WordleClientException | None,
    basic_wordle_client: WordleClient,
):
    response = Response
    response.status_code = status_code
    response.reason = reason
    first_side_effect = check_http_status_side_effect or check_response_status_side_effect
    expected_message = str(first_side_effect)

    with pytest.raises(WordleClientException) as exc_info:
        basic_wordle_client.process_response(response=response, response_type=response_type)

    assert str(exc_info.value) == expected_message


# @mock.patch.object(WordleClient, "check_http_status")
# @mock.patch.object(WordleClient, "check_response_status")
# def test_process_response_success():
#     response = Response


# def process_response(self, response: Response, response_type: Type[GenericResponse]) -> GenericResponse:
#     self.check_http_status(response)
#     parsed_response = response_type(**json.loads(response.text))
#     self.check_response_status(parsed_response)
#     return parsed_response
