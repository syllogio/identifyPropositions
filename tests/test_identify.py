from identifyPropositions import identify
from unittest.mock import patch
import spacy


def test_syllogism():
    assert identify("All men are mortal. Greeks are men. Greeks are mortal") == [
        "All men are mortal",
        "Greeks are men",
        "Greeks are mortal",
    ]


@patch("spacy.load", return_value=spacy.load("en_core_web_sm"))
def test_with_model(spacy_load):
    assert identify(
        "All men are mortal. Greeks are men. Greeks are mortal",
        model_name="some_other_model",
    ) == ["All men are mortal", "Greeks are men", "Greeks are mortal"]
    spacy_load.assert_called_once_with("some_other_model")


def test_compound():
    assert identify(
        "I am a human and all humans are mortal. Therefore, I am mortal"
    ) == ["all humans are mortal", "I am a human", "Therefore, I am mortal"]


def test_compound_non_auxiliary():
    assert identify("I am a human, and humans eat food. Therefore, I eat food") == [
        "humans eat food",
        "I am a human",
        "Therefore, I eat food",
    ]


def test_compound_with_since():
    assert identify(
        "I drink water since I am a human, and all humans drink water."
    ) == ["since I am a human", "all humans drink water", "I drink water"]


def test_em_dash():
    assert identify("All men are mortal — Socrates is a man — Socrates is mortal.") == [
        "All men are mortal",
        "Socrates is a man",
        "Socrates is mortal",
    ]


def test_new_line():
    assert (
        identify(
            """
        All men are mortal.
        Socrates is a man.
        Socrates is mortal.
        """
        )
        == ["All men are mortal", "Socrates is a man", "Socrates is mortal"]
    )
