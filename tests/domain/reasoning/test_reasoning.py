import pytest

from blueprint_forge import (
    Reasoning,
    VALID_REASONING_STATES,
    InvalidReasoningStatus,
)

from tests.factories.DataFactories import ReasoningDataFactory

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(ReasoningDataFactory(status="in_progress"), id="in_progress_status"),
        pytest.param(ReasoningDataFactory(status="complete"), id="complete_status"),
    ],
)

def test_Reasoning_accepts_vaild_inputs(data):
    Reasoning(**data)

@pytest.mark.parametrize(
    "data, expected_received",
    [
        pytest.param(
            ReasoningDataFactory(status="invalid"),
            "invalid",
            id="invalid_string",
        ),
        pytest.param(
            ReasoningDataFactory(status=""),
            "",
            id="empty_string_status",
        ),
    ],
)

def test_Reasoning_rejects_invalid_inputs(data, expected_received):
    with pytest.raises(InvalidReasoningStatus) as exc_info:
        Reasoning(**data)

    assert exc_info.value.received == expected_received
    assert exc_info.value.expected == VALID_REASONING_STATES

