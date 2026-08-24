from typing import List

from blueprint_forge import (
    Question,
    GraphvizRenderer,
    GraphvizApplication,
    GraphvizConfig,
    GraphvizGraph,
)

def test_GraphVizRenderer_renders_correctly(questions: List[Question]):
    # Setup
    renderer = GraphvizRenderer()

    config = GraphvizConfig(
        header="HEADER",
        footer="FOOTER",
    )
    graph = GraphvizGraph.from_questions(questions=questions)

    # Execution
    output = renderer.render(
        graph=graph,
        config=config,
        )

    # Validation
    assert isinstance(output, str)

    assert output.startswith("HEADER")
    assert output.endswith("FOOTER")

    for node in graph.nodes:
        assert node.to_graphviz() in output

    for edge in graph.edges:
        assert edge.to_graphviz() in output

def test_GraphvizApplication_generates_dot_file(tmp_path):
    # Setup
    yaml_path = tmp_path / "questions.yaml"
    header_path = tmp_path / "header.dot"
    footer_path = tmp_path / "footer.dot"
    output_path = tmp_path / "output.dot"

    yaml_path.write_text(
        """
        questions:
          node_1:
            question: "What is engineering information?"
            summary: "Test summary"
            reasoning:
              status: "complete"
              worksheet_path: "reasoning/test.md"
            knowledge:
              type: "adr"
              path: "knowledge/test.md"
            prerequisites: []

          node_2:
            question: "What is an ADR?"
            summary: "Test summary"
            reasoning:
              status: "complete"
              worksheet_path: "reasoning/test2.md"
            knowledge:
              type: "adr"
              path: "knowledge/test2.md"
            prerequisites:
              - node_1
        """
    )

    header_path.write_text("HEADER")
    footer_path.write_text("FOOTER")

    application = GraphvizApplication()

    # Execution
    application.generate(
        yaml_path=yaml_path,
        header_path=header_path,
        footer_path=footer_path,
        output_path=output_path,
    )

    # Validation
    assert output_path.exists()

    output = output_path.read_text()

    assert output.startswith("HEADER")
    assert output.endswith("FOOTER")

    assert "node_1" in output
    assert "node_2" in output
    assert 'label="What' in output
    assert "node_1 -> node_2" in output
