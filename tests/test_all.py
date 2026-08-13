import pytest
from typing import List

from src import (
    Question,
    Reasoning,
    Knowledge,
    GraphvizGraph,
    GraphvizNode,
    GraphvizEdge,
    GraphvizRenderer,
    GraphvizConfig,
    YAMLParser,
    GraphvizConfigLoader,
    GraphvizFileWriter,
    GraphvizApplication,
)

from tests.factories.DataFactories import (
    QuestionDataFactory,
    QuestionWithoutKnowledgeDataFactory,
    QuestionWithoutWorksheetPathDataFactory,
    ReasoningDataFactory,
)

def test_QuestionDataFactory_create_successfully():
    data = QuestionDataFactory()

    question_id = next(iter(data))
    question_data = data[question_id]

    assert question_id.startswith("node_")

    assert question_data["question"] == "Test question"
    assert question_data["summary"] == "Test summary"

    assert question_data["reasoning"]["status"] == "complete"
    assert question_data["reasoning"]["worksheet_path"] == (
        f"reasoning/worksheets/{question_id}.md"
    )

    assert question_data["knowledge"]["type"] == "adr"
    assert question_data["knowledge"]["path"] == (
        f"knowledge/adrs/{question_id}.md"
    )

    assert question_data["prerequisites"] == []

def test_Question_from_dict_create_successful():
    # Setup
    data = QuestionDataFactory()
    question_id, question_data = next(iter(data.items()))

    # Execution
    question = Question.from_dict(
        id=question_id,
        data=question_data
        )

    # Verification
    assert question.id == question_id
    assert question.question == question_data["question"]
    assert question.summary == question_data["summary"]

    assert isinstance(question.reasoning, Reasoning)
    assert question.reasoning.status == question_data["reasoning"]["status"]
    assert question.reasoning.worksheet_path == question_data["reasoning"]["worksheet_path"]

    assert isinstance(question.knowledge, Knowledge)
    assert question.knowledge.type == question_data["knowledge"]["type"]
    assert question.knowledge.path == question_data["knowledge"]["path"]

    assert question.prerequisites == question_data["prerequisites"]

def test_question_from_dict_none_knowledge_section_generation():
    # Setup
    data = QuestionDataFactory(knowledge=None)
    question_id, question_data = next(iter(data.items()))

    # Execution
    question = Question.from_dict(
        id=question_id,
        data=question_data
        )

    # Verification
    assert question.id == question_id
    assert question.question == question_data["question"]
    assert question.summary == question_data["summary"]

    assert isinstance(question.reasoning, Reasoning)
    assert question.reasoning.status == question_data["reasoning"]["status"]
    assert question.reasoning.worksheet_path == question_data["reasoning"]["worksheet_path"]

    assert question.knowledge == None

    assert question.prerequisites == question_data["prerequisites"]

def test_question_from_dict_absent_knowledge_section_generation():
    # Setup
    data = QuestionWithoutKnowledgeDataFactory()
    question_id, question_data = next(iter(data.items()))

    # Execution
    question = Question.from_dict(
        id=question_id,
        data=question_data
        )

    # Verification
    assert question.id == question_id
    assert question.question == question_data["question"]
    assert question.summary == question_data["summary"]

    assert isinstance(question.reasoning, Reasoning)
    assert question.reasoning.status == question_data["reasoning"]["status"]
    assert question.reasoning.worksheet_path == question_data["reasoning"]["worksheet_path"]

    assert question.knowledge == None

    assert question.prerequisites == question_data["prerequisites"]

def test_question_from_dict_absent_worksheet_path_generation():
    # Setup
        data = QuestionWithoutWorksheetPathDataFactory()

        question_id, question_data = next(iter(data.items()))
    
        # Execution
        question = Question.from_dict(
            id=question_id,
            data=question_data
            )

        # Verification
        assert question.id == question_id
        assert question.question == question_data["question"]
        assert question.summary == question_data["summary"]
    
        assert isinstance(question.reasoning, Reasoning)
        assert question.reasoning.status == question_data["reasoning"]["status"]
        assert question.reasoning.worksheet_path == None
    
        assert isinstance(question.knowledge, Knowledge)
        assert question.knowledge.type == question_data["knowledge"]["type"]
        assert question.knowledge.path == question_data["knowledge"]["path"]
    
        assert question.prerequisites == question_data["prerequisites"]

def test_question_from_dict_none_worksheet_path_generation():
    # Setup
        data = QuestionDataFactory(
            reasoning=ReasoningDataFactory(
                worksheet_path=None
            )
        )

        question_id, question_data = next(iter(data.items()))
    
        # Execution
        question = Question.from_dict(
            id=question_id,
            data=question_data
            )

        # Verification
        assert question.id == question_id
        assert question.question == question_data["question"]
        assert question.summary == question_data["summary"]
    
        assert isinstance(question.reasoning, Reasoning)
        assert question.reasoning.status == question_data["reasoning"]["status"]
        assert question.reasoning.worksheet_path == None
    
        assert isinstance(question.knowledge, Knowledge)
        assert question.knowledge.type == question_data["knowledge"]["type"]
        assert question.knowledge.path == question_data["knowledge"]["path"]
    
        assert question.prerequisites == question_data["prerequisites"]

def test_GraphvizNode_generates_from_question_correctly(question: Question):
    # Execution
    node = GraphvizNode.from_question(question=question)

    # Validation
    assert isinstance(node, GraphvizNode)
    assert node.id == question.id
    assert node.label == question.question
    assert node.shape == "box"

def test_GraphvizNode_to_graphviz_generates_correctly(question: Question):
    # Setup
    node = GraphvizNode.from_question(question=question)

    # Execution
    output = node.to_graphviz()

    # Validation
    assert output == (f'{node.id} [\n'
            f'    label="{node.label}"\n'
            f'    shape={node.shape}\n'
            f']'
    )

@pytest.mark.parametrize(
    "knowledge_type, expected_shape",
    [
        pytest.param("adr", "box", id="adr"),
        pytest.param("classification", "diamond", id="classification"),
        pytest.param(None, "oval", id="no-knowledge"),
    ],
)

def test_GraphvizNode_determines_shape(
    question: Question,
    knowledge_type: str | None,
    expected_shape: str,
):
    if knowledge_type is None:
        question.knowledge = None
    else:
        question.knowledge.type = knowledge_type

    assert (
        GraphvizNode.determine_shape(question)
        == expected_shape
    )

def test_GraphvizEdge_to_graphviz_generates_correctly():
    # Setup
    edge = GraphvizEdge(
        start_node="node_2",
        end_node="node_1",
    )

    # Execution
    output = edge.to_graphviz()

    # Validation
    assert output == "node_2 -> node_1"

def test_GraphvizGraph_generates_from_list_of_questions(questions: List[Question]):
    # Execution
    graph = GraphvizGraph.from_questions(questions=questions)

    # Validation
    assert isinstance(graph, GraphvizGraph)
    for node in graph.nodes:
        assert isinstance(node, GraphvizNode)
    for edge in graph.edges:
        assert isinstance(edge, GraphvizEdge)
    assert len(graph.nodes) == len(questions)
    assert len(graph.edges) > 0

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
    assert 'label="What is engineering information?"' in output
    assert 'label="What is an ADR?"' in output
    assert "node_1 -> node_2" in output
