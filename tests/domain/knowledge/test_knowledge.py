import pytest

from blueprint_forge import (
    Knowledge,
    VALID_KNOWLEDGE_TYPES,
    InvalidKnowledgeType,
)

from tests.factories.DataFactories import KnowledgeDataFactory

@pytest.mark.parametrize(
    "data",
    [
        pytest.param(KnowledgeDataFactory(type="adr"), id="adr_type"),
        pytest.param(KnowledgeDataFactory(type="classification"), id="classification_type"),
    ],
)

def test_Knowledge_with_vaild_inputs(data):
    Knowledge(**data)

@pytest.mark.parametrize(
    "data, expected_received",
    [
        pytest.param(
            KnowledgeDataFactory(type="invalid"),
            "invalid",
            id="invalid_string",
        ),
        pytest.param(
            KnowledgeDataFactory(type=""),
            "",
            id="empty_string",
        ),
    ],
)

def test_Knowledge_rejects_invalid_types(data, expected_received):
    with pytest.raises(InvalidKnowledgeType) as exc_info:
        Knowledge(**data)

    assert exc_info.value.received == expected_received
    assert exc_info.value.expected == VALID_KNOWLEDGE_TYPES

