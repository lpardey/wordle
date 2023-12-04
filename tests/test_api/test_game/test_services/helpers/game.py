# Dependencies
import pytest

# From apps
from api.v1.game.services.resources.schemas import LetterStatus


def compare_test_data() -> list[pytest.param]:
    return [
        pytest.param(
            "APPLE",
            "APPLE",
            [LetterStatus.IN_PLACE] * 5,
            id="All letters in place",
        ),
        pytest.param(
            "PIZZA",
            "WORLD",
            [LetterStatus.NOT_PRESENT] * 5,
            id="All letters not present",
        ),
        pytest.param(
            "OOOOO",
            "COACH",
            [LetterStatus.NOT_PRESENT, LetterStatus.IN_PLACE] + [LetterStatus.NOT_PRESENT] * 3,
            id="In place: [2, 0, 2, 2, 2]",
        ),
        pytest.param(
            "ONION",
            "SOURS",
            [LetterStatus.PRESENT] + [LetterStatus.NOT_PRESENT] * 4,
            id="Present: [1, 2, 2, 2, 2]",
        ),
        pytest.param(
            "LLAAA",
            "ODDLL",
            [LetterStatus.PRESENT] * 2 + [LetterStatus.NOT_PRESENT] * 3,
            id="Present: [1, 1, 2, 2, 2]",
        ),
        pytest.param(
            "LALAA",
            "OLDLS",
            [LetterStatus.PRESENT, LetterStatus.NOT_PRESENT] * 2 + [LetterStatus.NOT_PRESENT],
            id="Present: [1, 2, 1, 2, 2]",
        ),
        pytest.param(
            "LLLAA",
            "OCLLL",
            [LetterStatus.PRESENT] * 2 + [LetterStatus.IN_PLACE] + [LetterStatus.NOT_PRESENT] * 2,
            id="Present repeated: [1, 1, 0, 2, 2]",
        ),
        pytest.param(
            "LLASL",
            "OLLLS",
            [LetterStatus.PRESENT, LetterStatus.IN_PLACE, LetterStatus.NOT_PRESENT] + [LetterStatus.PRESENT] * 2,
            id="Present repeated: [1, 0, 2, 1, 1]",
        ),
        pytest.param(
            "EMBER",
            "QUEEN",
            [LetterStatus.PRESENT]
            + [LetterStatus.NOT_PRESENT] * 2
            + [LetterStatus.IN_PLACE, LetterStatus.NOT_PRESENT],
            id="Present repeated: [1, 2, 2, 0, 2]",
        ),
        pytest.param(
            "EMBER",
            "FLYER",
            [LetterStatus.NOT_PRESENT] * 3 + [LetterStatus.IN_PLACE] * 2,
            id="Repeated: [2, 2, 2, 0, 0]",
        ),
    ]
