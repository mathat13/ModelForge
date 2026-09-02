import pytest

from tests.factories.DataFactories import (
    QuestionYamlFactory,
    ReasoningDataFactory,
    KnowledgeDataFactory,
)

from blueprint_forge import (
    Question,
    Reasoning,
    Knowledge,
    InvalidQuestionID,
    InvalidQuestionState,
)

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(
            QuestionYamlFactory(),
            id="all_fields",
        ),
        pytest.param(
            QuestionYamlFactory(
                reasoning=ReasoningDataFactory(),
                knowledge=None,
            ),
            id="no_knowledge",
        ),
        pytest.param(
            QuestionYamlFactory(
                reasoning=ReasoningDataFactory(worksheet_path=None),
                knowledge=KnowledgeDataFactory(),
            ),
            id="no_reasoning_worksheet_path",
        ),
    ],
)

def test_Question_accepts_valid_data(data):

    question_id, question_data = next(iter(data.items()))

    question = Question.from_dict(id=question_id,
                        data=question_data
                        )

    # Verification
    assert question.id == question_id
    assert question.question == question_data["question"]
    assert question.summary == question_data["summary"]

    assert isinstance(question.reasoning, Reasoning)
    assert question.reasoning.status == question_data["reasoning"]["status"]
    assert question.reasoning.worksheet_path == question_data["reasoning"].get("worksheet_path")

    if isinstance(question.knowledge, Knowledge):
        assert question.knowledge.type == question_data["knowledge"]["type"]
        assert question.knowledge.path == question_data["knowledge"]["path"]
    else:
        assert question.knowledge == None
    
    assert question.prerequisites == question_data["prerequisites"]

@pytest.mark.parametrize(
    "question_yaml",
    [
        pytest.param(QuestionYamlFactory(id="node_1"), id="non-empty_string_id"),
    ],
)

def test_Question_accepts_valid_id(question_yaml):
    # Setup
    question_id, question_data = next(iter(question_yaml.items()))
    Question.from_dict(id=question_id,
                       data=question_data
                       )

@pytest.mark.parametrize(
    "question_yaml, expected_received",
    [
        pytest.param(
            QuestionYamlFactory(id=123),
            123,
            id="non-string_id",
        ),
        pytest.param(
            QuestionYamlFactory(id=""),
            "",
            id="empty_string_id",
        ),
    ],
)

def test_Question_rejects_invalid_id(question_yaml, expected_received):
    # Setup
    question_id, question_data = next(iter(question_yaml.items()))

    # Validation
    with pytest.raises(InvalidQuestionID) as exc_info:
        Question.from_dict(id=question_id,
                           data=question_data
                           )

    assert exc_info.value.received == expected_received

@pytest.mark.parametrize(
    "states",
    [
        pytest.param(
            QuestionYamlFactory(
                reasoning=ReasoningDataFactory(status="complete"),
                knowledge=None,
            ),
            id="reasoning.status=complete+no_knowledge"
        ),
        pytest.param(
            QuestionYamlFactory(
                reasoning=ReasoningDataFactory(status="complete"),
                knowledge=KnowledgeDataFactory(),
            ),
            id="reasoning.status=complete+knowledge"
        ),
        pytest.param(
            QuestionYamlFactory(
                reasoning=ReasoningDataFactory(status="in_progress"),
                knowledge=None
            ),
            id="reasoning.status=in_progress+no_knowledge"
        ),
    ],
)

def test_Question_accepts_valid_states(states):
    # Setup
    question_id, question_data = next(iter(states.items()))

    # Execution
    Question.from_dict(
        id=question_id,
        data=question_data
        )

def test_Question_rejects_invalid_states():
    # Setup
    data = QuestionYamlFactory(
        reasoning=ReasoningDataFactory(status="in_progress"),
        knowledge=KnowledgeDataFactory()
        )
    
    question_id, question_data = next(iter(data.items()))

    # Validation
    with pytest.raises(InvalidQuestionState) as exc_info:
        Question.from_dict(
            id=question_id,
            data=question_data
            )

    assert "reasoning" in exc_info.value.reason

    
