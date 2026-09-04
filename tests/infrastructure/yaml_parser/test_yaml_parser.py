import pytest

from blueprint_forge import (
    YAMLParser,
    YAMLFileNotFound,
)

def test_YAMLParser_accepts_existing_file(tmp_path):
    yaml_path = tmp_path / "test.yaml"

    yaml_path.write_text(
        """
        questions:
          test:
            question: "Test question"
            summary: "Test summary"
            prerequisites: []
        """
    )

    # Execution
    YAMLParser.parse(yaml_path)

def test_YAMLParser_rejects_missing_file(tmp_path):
    # Setup
    yaml_path = tmp_path / "test.yaml"

    # Execution
    with pytest.raises(YAMLFileNotFound) as exc_info:
        YAMLParser.parse(yaml_path)
        

    assert yaml_path.as_posix() in str(exc_info.value)
    assert exc_info.value.path == yaml_path