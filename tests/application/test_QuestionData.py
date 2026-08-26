import pytest
from pydantic import (
    ValidationError,
)

from blueprint_forge import QuestionData

from tests.factories.DataFactories import (
    QuestionDataFactory,
    ReasoningDataFactory,
    QuestionDataWithoutKnowledgeFactory,
    QuestionDataWithoutReasoningFactory,
    QuestionDataWithoutReasoningStatusFactory,
    QuestionDataWithoutQuestionFactory,
    QuestionDataWithoutSummaryFactory,
)

'''
Behaviour Table

Field                       Valid             Invalid
---------------------------------------------------------------
question                    string            null / non-string
summary                     string            null / non-string
reasoning                   object            null / absent
reasoning.status            string            null / absent
reasoning.worksheet_path    string / absent   wrong type
knowledge                   object / absent   malformed
prerequisites               list[str]         wrong type
extra fields                --                forbidden
'''

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(QuestionDataFactory(knowledge=None), id="null_knowledge"),
        pytest.param(QuestionDataWithoutKnowledgeFactory(), id="no_knowledge"),

    ],
)

def test_QuestionData_validates_on_valid_data(data):
    QuestionData.model_validate(data)

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(QuestionDataFactory(reasoning=ReasoningDataFactory(status=None)), id="null_reasoning_status"),
        pytest.param(QuestionDataFactory(question=None), id="null_question"),
        pytest.param(QuestionDataFactory(summary=None), id="null_summary"),
        pytest.param(QuestionDataFactory(reasoning=None),id="null_reasoning"),
    ],
)

def test_QuestionData_raises_ValidationError_on_null_required_data(data):
    with pytest.raises(ValidationError):
        QuestionData.model_validate(data)

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(QuestionDataWithoutReasoningStatusFactory(), id="no_reasoning_status"),
        pytest.param(QuestionDataWithoutQuestionFactory(), id="no_question"),
        pytest.param(QuestionDataWithoutSummaryFactory(), id="no_summary"),
        pytest.param(QuestionDataWithoutReasoningFactory(), id="no_reasoning"),
    ],
)

def test_QuestionData_raises_ValidationError_on_missing_required_data(data):
    with pytest.raises(ValidationError):
        QuestionData.model_validate(data)

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(QuestionDataFactory(question=123), id="incorrect_question_type"),
        pytest.param(QuestionDataFactory(summary=123), id="incorrect_summary_type"),
    ],
)

def test_QuestionData_raises_ValidationError_on_incorrect_field_types(data):
    with pytest.raises(ValidationError):
        QuestionData.model_validate(data)

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(QuestionDataFactory(prerequisites=["node_1", "node_2"]), id="list_of_strings"),
        pytest.param(QuestionDataFactory(prerequisites=[]), id="empty_list"),
    ],
)

def test_QuestionData_accepts_valid_prerequisites(data):
    QuestionData.model_validate(data)
    
@pytest.mark.parametrize(
    "data",
    [
        pytest.param(QuestionDataFactory(prerequisites=[1,2]), id="incorrect_list_types"),
        pytest.param(QuestionDataFactory(prerequisites=1), id="incorrect_prerequisite_type"),
    ],
)

def test_QuestionData_rejects_invalid_prerequisites(data):
    with pytest.raises(ValidationError):
        QuestionData.model_validate(data)

def test_QuestionData_raises_ValidationError_on_extra_fields():
    data = QuestionDataFactory()
    data["extra_field"] = 33

    with pytest.raises(ValidationError):
            QuestionData.model_validate(data)