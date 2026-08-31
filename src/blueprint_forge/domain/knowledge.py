from dataclasses import dataclass

from blueprint_forge.domain.exceptions.domain_exceptions import InvalidKnowledgeType

VALID_KNOWLEDGE_TYPES = frozenset({"adr", "classification"})
@dataclass(frozen=True)
class Knowledge:
    type: str
    path: str 

    def __post_init__(self):
        if self.type not in VALID_KNOWLEDGE_TYPES:
            raise InvalidKnowledgeType(received=self.type,
                                       expected=VALID_KNOWLEDGE_TYPES,
                                       )