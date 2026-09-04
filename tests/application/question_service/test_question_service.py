import pytest
from pathlib import Path

from blueprint_forge import (
    YAMLParser,
    QuestionService,
    InvalidQuestionSourceData,
)

@pytest.mark.parametrize(
    "parsed_data",
    [
        pytest.param(None, id="null-dictionary"),
        pytest.param(["questions"], id="non-dictionary"),
        pytest.param({}, id="empty_dictionary"),
        pytest.param({"cat": 1}, id="no_questions_key"),
        pytest.param({"questions": None}, id="null_questions_value"),
        pytest.param({"questions": {}}, id="no_questions_value"),
    ]
)

def test_QuestionService_load_rejects_invalid_data(mocker, parsed_data):
    # Setup

    yaml_path = Path("test.yaml")

    mocker.patch.object(
        YAMLParser,
        "parse",
        return_value=parsed_data,
    )

    service = QuestionService()

    # Execution
    with pytest.raises(InvalidQuestionSourceData) as exc_info:
        service.load(yaml_path=yaml_path)

    assert exc_info.value.received == parsed_data