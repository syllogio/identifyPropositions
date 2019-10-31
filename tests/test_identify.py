from identifyPropositions import identifyText
from unittest.mock import patch
import spacy


def test_syllogism():
    assert identifyText("All men are mortal. Greeks are men. Greeks are mortal") == [
        "All men are mortal",
        "Greeks are men",
        "Greeks are mortal",
    ]


@patch("spacy.load", return_value=spacy.load("en_core_web_sm"))
def test_with_model(spacy_load):
    assert identifyText(
        "All men are mortal. Greeks are men. Greeks are mortal",
        model_name="some_other_model",
    ) == ["All men are mortal", "Greeks are men", "Greeks are mortal"]
    spacy_load.assert_called_once_with("some_other_model")


def test_compound():
    assert identifyText(
        "I am a human and all humans are mortal. Therefore, I am mortal"
    ) == ["all humans are mortal", "I am a human", "Therefore, I am mortal"]


def test_compound_non_auxiliary():
    assert identifyText("I am a human, and humans eat food. Therefore, I eat food") == [
        "humans eat food",
        "I am a human",
        "Therefore, I eat food",
    ]


def test_compound_with_since():
    assert identifyText(
        "I drink water since I am a human, and all humans drink water."
    ) == ["since I am a human", "all humans drink water", "I drink water"]


def test_em_dash():
    assert identifyText(
        "All men are mortal — Socrates is a man — Socrates is mortal."
    ) == ["All men are mortal", "Socrates is a man", "Socrates is mortal"]


def test_new_line():
    assert (
        identifyText(
            """
        All men are mortal.
        Socrates is a man.
        Socrates is mortal.
        """
        )
        == ["All men are mortal", "Socrates is a man", "Socrates is mortal"]
    )


def test_adverbial_clause_without_nominal_subject():
    assert (
        identifyText(
            """
        Looking forward beyond the stimulus, we need a very different sort of economy, one that restores a balanced form of capitalism. At the core of this change is a long-term increase in public outlay, investing in areas vital to economic growth and social decency. [...] An enhanced federal role, in turn, provides the moment to reclaim the public philosophy of activist government that effectively services people's needs where market forces fail.
        """  # noqa: E501
        )
        == [
            "Looking forward beyond the stimulus, we need a very different sort of economy, one that restores a balanced form of capitalism",  # noqa: E501
            "At the core of this change is a long-term increase in public outlay, investing in areas vital to economic growth and social decency",  # noqa: E501
            "An enhanced federal role, in turn, provides the moment to reclaim the public philosophy of activist government that effectively services people's needs where market forces fail",  # noqa: E501
        ]
    )
