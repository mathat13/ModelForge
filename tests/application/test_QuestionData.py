import pytest
from pydantic import (
    ValidationError,
)

from blueprint_forge import QuestionData

from tests.factories.DataFactories import (
    QuestionDataFactory,
    ReasoningDataFactory,
    QuestionDataWithoutReasoningFactory,
    QuestionDataWithoutReasoningStatusFactory,
    QuestionDataWithoutQuestionFactory,
    QuestionDataWithoutSummaryFactory,
)

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(QuestionDataFactory(reasoning=ReasoningDataFactory(status=None)), id="no_reasoning_status"),
        pytest.param(QuestionDataFactory(question=None), id="no_question"),
        pytest.param(QuestionDataFactory(summary=None), id="no_summary"),
        pytest.param(QuestionDataFactory(reasoning=None),id="no_reasoning"),
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

def test_QuestionData_raises_ValidationError_on_wrong_question_field_types(data):
    with pytest.raises(ValidationError):
        QuestionData.model_validate(data)

def test_QuestionData_raises_ValidationError_on_incorrect_prerequisites_type():
    data = QuestionDataFactory(prerequisites=[1,2])
    with pytest.raises(ValidationError):
        QuestionData.model_validate(data)

def test_QuestionData_raises_ValidationError_on_extra_fields():
    data = QuestionDataFactory()
    data["extra_field"] = 33

    with pytest.raises(ValidationError):
            QuestionData.model_validate(data)