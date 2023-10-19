from random import randint
import re
from typing import Callable
import requests
import logging
from functools import partial

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
            cls._words = get_words_list()

        return cls._words


def get_words_list() -> list[str]:
    # con esta no funcionaran los tests si no tienes internet : )
    # return get_words_list_from_meaningpedia()
    return get_words_list_v2(ALL_WORD_SOURCES)


def get_words_list_v1() -> list[str]:
    internet_words: list[str] = []

    try:
        internet_words = get_words_list_from_meaningpedia()
    except Exception as e:
        logger.exception(e)

    local_words = get_words_list_from_static_content()
    local_extra_words = get_words_list_from_static_content(STATIC_EXTRA_WORDS_LIST_FILE)
    all_words = list(set(internet_words) | set(local_words) | set(local_extra_words))
    return all_words


def get_words_list_v2(words_source_functions: list[WordSourceFunction]) -> list[str]:
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

    # get list of words by grabbing regex captures of response
    # there's probably a far better way to do this by actually parsing the HTML
    # response, but I don't know how to do that, and this gets the job done

    # compile regex
    pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
    # find all matches
    words_list: list[str] = pattern.findall(response.text)
    parsed_words_list = [word.upper() for word in words_list]
    return parsed_words_list


def get_game_word(words_list: list[str]) -> str:
    index = randint(a=0, b=len(words_list))
    game_word = words_list[index]
    return game_word


ALL_WORD_SOURCES = [
    get_words_list_from_meaningpedia,
    get_words_list_from_static_content,
    partial(get_words_list_from_static_content, STATIC_EXTRA_WORDS_LIST_FILE),
]
