import pytest
from typing import List

from blueprint_forge import (
    Question,
    QuestionCollection,
    GraphvizEdge,
    GraphvizGraph,
    GraphvizNode,
)

from tests.factories.DataFactories import (
    KnowledgeDataFactory,
    ReasoningDataFactory,
    QuestionYamlFactory,
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
    "question_yaml, expected_shape",
    [
        pytest.param(QuestionYamlFactory(knowledge=KnowledgeDataFactory(type="adr")), "box", id="adr->box"),
        pytest.param(QuestionYamlFactory(knowledge=KnowledgeDataFactory(type="classification")), "diamond", id="classification->diamond"),
        pytest.param(QuestionYamlFactory(knowledge=None), "oval", id="no-knowledge->oval"),
    ],
)

def test_GraphvizNode_determines_shape(
    question_yaml: dict,
    expected_shape: str,
):
    # Setup
    question_id, question_data = next(iter(question_yaml.items()))
    question = Question.from_dict(id=question_id,
                                  data=question_data
                                  )

    # Verification
    assert (
        GraphvizNode.determine_shape(question)
        == expected_shape
    )

@pytest.mark.parametrize(
    "question_yaml, expected_peripheries",
    [
        pytest.param(
            QuestionYamlFactory(
                reasoning=ReasoningDataFactory(status="in_progress"),
                knowledge=None
            ),
            None,
            id="incomplete-reasoning-no-knowledge",
        ),
        pytest.param(
            QuestionYamlFactory(
                reasoning=ReasoningDataFactory(status="complete"),
                knowledge=KnowledgeDataFactory()
            ),
            None,
            id="complete-reasoning-with-knowledge"
        ),
        pytest.param(
            QuestionYamlFactory(
                reasoning=ReasoningDataFactory(status="complete"),
                knowledge=None
            ),
            2, 
            id="complete-reasoning-no-knowledge"
        ),
    ],
)

def test_GraphvizNode_determines_peripheries(
    question_yaml: dict,
    expected_peripheries: int,
):
    # Setup
    question_id, question_data = next(iter(question_yaml.items()))
    question = Question.from_dict(id=question_id,
                                  data=question_data
                                  )

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
    # Setup
    question_collection = QuestionCollection(questions=questions)
    # Execution
    graph = GraphvizGraph.from_question_collection(collection=question_collection)

    # Validation
    assert isinstance(graph, GraphvizGraph)
    for node in graph.nodes:
        assert isinstance(node, GraphvizNode)
    for edge in graph.edges:
        assert isinstance(edge, GraphvizEdge)
    assert len(graph.nodes) == len(questions)
    assert len(graph.edges) > 0