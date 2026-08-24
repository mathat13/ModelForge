import pytest
from typing import List

from blueprint_forge import (
    Question,
    GraphvizEdge,
    GraphvizGraph,
    GraphvizNode,
    Knowledge,
)

from tests.factories.DataFactories import (
    KnowledgeDataFactory,
)

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

@pytest.mark.parametrize(
    "reasoning_status, knowledge, expected_peripheries",
    [
        pytest.param("complete", None, 2, id="reasoning-artifact"),
        pytest.param("complete", KnowledgeDataFactory(), None, id="knowledge-artifact"),
        pytest.param("in_progress", None, None, id="no-artifact"),
    ],
)

def test_GraphvizNode_determines_peripheries(
    question: Question,
    reasoning_status: str,
    knowledge: Knowledge | None,
    expected_peripheries: int,
):
    # Setup
    if knowledge is None:
            question.knowledge = None
    else:
        question.knowledge = knowledge

    question.reasoning.status = reasoning_status

    # Execution/ Validation
    assert (
        GraphvizNode.determine_peripheries(question=question)
        == expected_peripheries
    )

@pytest.mark.parametrize(
    "label, width, expected",
    [
        pytest.param(
            "What is repository documentation?",
            25,
            "What is repository\\ndocumentation?",
            id="breaks-at-word",
        ),
        pytest.param(
            "Short question",
            25,
            "Short question",
            id="does-not-break-short-label",
        ),
        pytest.param(
            "What is the authoritative source for each engineering information type?",
            25,
            "What is the authoritative\\nsource for each\\nengineering information\\ntype?",
            id="multiple-lines",
        ),
    ],
)

def test_GraphvizNode_formats_label(
    label: str,
    width: int,
    expected: str,
):
    assert GraphvizNode.format_label(
        label=label,
        width=width,
    ) == expected
    
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