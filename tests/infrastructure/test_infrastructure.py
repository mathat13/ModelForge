from blueprint_forge import (
    GraphvizFileWriter,
)

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