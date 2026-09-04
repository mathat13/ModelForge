#--- Knowledge

class InvalidKnowledgeType(Exception):
    def __init__(self, received: str, expected: str):
        super().__init__(
            f"Knowledge artifact of type '{received}'. "
            f"Expected one of: {', '.join(sorted(expected))}"
        )
        self.expected=expected
        self.received=received

#--- Reasoning

class InvalidReasoningStatus(Exception):
    def __init__(self, received: str, expected: str):
        super().__init__(
            f"Received reasoning status: '{received}'. "
            f"Expected one of: {', '.join(sorted(expected))}"
        )
        self.expected=expected
        self.received=received

# --- Question

class InvalidQuestionID(Exception):
    def __init__(self, received):
        super().__init__(
            f"Received ID: '{received}'. "
            f"Expected a non-empty string."
        )
        self.received=received

class InvalidQuestionState(Exception):
    def __init__(self, reason: str, received):
        self.reason = reason
        self.received = received

        super().__init__(
            f"Invalid question state: {reason}. "
            f"Received: {received!r}"
        )

# --- QuestionCollection

class EmptyQuestionCollection(Exception):
    def __init__(self):

        super().__init__(
            f"Received empty question collection. "
            f"Expected at least one question."
        )

class DuplicateQuestionID(Exception):
    def __init__(self, question_id: str):
        self.question_id = question_id

        super().__init__(
            f"Duplicate question ID detected: {question_id}. "
        )

class InvalidPrerequisites(Exception):
    def __init__(self, reason: str):
        self.reason = reason

        super().__init__(
            f"Invalid prerequisites detected: "
            f"{reason}"
        )
