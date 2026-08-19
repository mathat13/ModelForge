from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner

from question_translator.presentation.cli import app

runner = CliRunner()

def test_cli_exposes_generate_command():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "generate" in result.stdout

def test_generate_requires_source():
    result = runner.invoke(app, ["generate"])

    assert result.exit_code != 0

def test_generate_exposes_source_argument():
    result = runner.invoke(app, ["generate", "--help"])

    assert result.exit_code == 0
    assert "source" in result.stdout

def test_generate_passes_source_to_application():
    mock_application = MagicMock()

    with patch(
        "question_translator.presentation.cli.GraphvizApplication",
        return_value=mock_application,
    ):
        result = runner.invoke(
            app,
            ["generate", "source.yaml"],
        )

    assert result.exit_code == 0

    mock_application.generate.assert_called_once()

    call = mock_application.generate.call_args

    assert call.kwargs["yaml_path"] == Path("source.yaml")


def test_generate_returns_error_when_command_is_invalid():
    result = runner.invoke(
        app,
        ["does-not-exist"],
    )

    assert result.exit_code != 0