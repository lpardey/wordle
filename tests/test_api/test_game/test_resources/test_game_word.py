# Standard Library
from unittest.mock import Mock, patch

# Dependencies
import pytest

# From apps
from api.v1.game.services.resources.game_word import ALL_WORD_SOURCES, AllWords


def test_words_property_initialization():
    result = AllWords.words

    assert result is not None


@patch("api.v1.game.services.resources.game_word.get_words_list", return_value=["CLOUD", "WIVES", "GUILT"])
def test_words(mock_get_words_list: Mock):
    AllWords._words = None
    expected_result = mock_get_words_list.return_value

    result = AllWords.words

    assert result == expected_result
    assert isinstance(result, list)
    mock_get_words_list.assert_called_once_with(ALL_WORD_SOURCES)


# @patch()
def test_get_words_list():
    ...
