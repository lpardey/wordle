import requests
from requests import Response


class WordleClientException(Exception):
    pass


class WordleClient:
    def __init__(self, service_url="http://localhost:8000") -> None:
        self.service_url = service_url
    