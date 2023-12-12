# Standard Library
import logging
import re
from random import randint
from typing import Callable

# Dependencies
import requests

logger = logging.getLogger(__name__)

STATIC_WORDS_LIST_FILE = "static/words.txt"
STATIC_EXTRA_WORDS_LIST_FILE = "static/extra_words.txt"

WordSourceFunction = Callable[[], list[str]]


class AllWords:
    _words: list[str] | None = None

    @classmethod
    @property
    def words(cls) -> list[str]:
        if cls._words is None:
            cls._words = get_words_list(ALL_WORD_SOURCES)

        return cls._words


def get_words_list(words_source_functions: list[WordSourceFunction]) -> list[str]:
    words_lists: list[list[str]] = []
    for source_function in words_source_functions:
        try:
            words_lists.append(source_function())
        except Exception as e:
            logger.exception(e)

    all_words = {word for words_list in words_lists for word in words_list}
    return list(all_words)


def get_words_list_from_static_content(filename: str = STATIC_WORDS_LIST_FILE) -> list[str]:
    with open(filename, "r") as f:
        words = [word.strip().upper() for word in f]
    return words


def get_words_list_from_meaningpedia() -> list[str]:
    url = "https://meaningpedia.com/5-letter-words?show=all"
    response = requests.get(url=url)
    pattern = re.compile(r'<span itemprop="name">(\w+)</span>')  # Compile regex
    words_list: list[str] = pattern.findall(response.text)  # Find all matches
    parsed_words_list = [word.upper() for word in words_list]
    return parsed_words_list


ALL_WORD_SOURCES = [get_words_list_from_meaningpedia, get_words_list_from_static_content]


def get_game_word(words_list: list[str]) -> str:
    index = randint(a=0, b=len(words_list))
    game_word = words_list[index]
    return game_word
