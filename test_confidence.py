import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from confidence import (
    confidence_level,
    calculate_confidence_v2
)


def test_high_confidence_level():

    assert confidence_level(0.9) == "High"


def test_medium_confidence_level():

    assert confidence_level(0.7) == "Medium"


def test_low_confidence_level():

    assert confidence_level(0.4) == "Low"


def test_confidence_v2_output_structure():

    scores = [0.1, 0.2, 0.3, 0.4]

    answer = (
        "This is a sufficiently long answer "
        "to test confidence generation."
    )

    result = calculate_confidence_v2(
        scores,
        answer
    )

    assert "score" in result
    assert "level" in result
    assert "reasons" in result
    assert isinstance(
        result["reasons"],
        list
    )