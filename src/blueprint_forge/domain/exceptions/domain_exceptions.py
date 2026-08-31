from typing import Literal

class InvalidKnowledgeType(Exception):
    def __init__(self, received: str, expected: str):
        super().__init__(
            f"Knowledge artifact of type '{received}'. "
            f"Expected one of: {', '.join(sorted(expected))}"
        )
        self.expected=expected
        self.received=received

class InvalidReasoningStatus(Exception):
    def __init__(self, received: str, expected: str):
        super().__init__(
            f"Received reasoning status: '{received}'. "
            f"Expected one of: {', '.join(sorted(expected))}"
        )
        self.expected=expected
        self.received=received