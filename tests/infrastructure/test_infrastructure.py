from modelforge import (
    GraphvizConfig,
    GraphvizConfigLoader,
    GraphvizFileWriter,
    YAMLParser
)

def test_YAMLParser_parses_yaml(tmp_path):
    # Setup
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
    data = YAMLParser.parse(yaml_path)

    # Validation
    assert data == {
        "questions": {
            "test": {
                "question": "Test question",
                "summary": "Test summary",
                "prerequisites": [],
            }
        }
    }

def test_GraphvizConfigLoader_loads_config(tmp_path):
    # Setup
    header_path = tmp_path / "header.dot"
    footer_path = tmp_path / "footer.dot"

    header_path.write_text("HEADER")
    footer_path.write_text("FOOTER")

    # Execution
    config = GraphvizConfigLoader.load(
        header_path=header_path,
        footer_path=footer_path,
    )

    # Validation
    assert isinstance(config, GraphvizConfig)
    assert config.header == "HEADER"
    assert config.footer == "FOOTER"

def test_GraphvizFileWriter_writes_file(tmp_path):
    # Setup
    output_path = tmp_path / "output.dot"
    output = "digraph {\n}"

    # Execution
    GraphvizFileWriter.write(
        output=output,
        path=output_path,
    )

    # Validation
    assert output_path.exists()
    assert output_path.read_text() == output