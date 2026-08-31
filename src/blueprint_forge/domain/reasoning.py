from dataclasses import dataclass

from blueprint_forge.domain.exceptions.domain_exceptions import InvalidReasoningStatus

VALID_REASONING_STATES = frozenset({"in_progress", "complete"})

@dataclass(frozen=True)
class Reasoning:
    status: str
    worksheet_path: str | None

    def __post_init__(self):
        if self.status not in VALID_REASONING_STATES:
            raise InvalidReasoningStatus(received=self.status,
                                        expected=VALID_REASONING_STATES,
                                        )