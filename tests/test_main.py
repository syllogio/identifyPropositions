from identifyPropositions.__main__ import main
from unittest.mock import patch
from imp import load_source


@patch("builtins.print")
def test_import(mock_print):
    main(["All men are mortal. Socrates is a man. Socrates is mortal."])
    mock_print.assert_called_once_with(
        """[
  "All men are mortal",
  "Socrates is a man",
  "Socrates is mortal"
]"""
    )


@patch("builtins.print")
def test_cli(mock_print):
    cliArgs = [
        "idpr",
        """All mammals are warm-blooded and all dogs are mammals.
        Therefore, all dogs are warm-blooded.""",
    ]
    with patch("sys.argv", cliArgs):
        load_source("__main__", "identifyPropositions/__main__.py")
        mock_print.assert_called_once_with(
            """[
  "all dogs are mammals",
  "All mammals are warm-blooded",
  "Therefore, all dogs are warm-blooded"
]"""
        )
