# Dependencies
import pytest

# From apps
from wordle_client.client import WordleClient


@pytest.fixture()
def basic_wordle_client() -> WordleClient:
    wordle_client = WordleClient(service_url="http://localhost:8000")
    return wordle_client
