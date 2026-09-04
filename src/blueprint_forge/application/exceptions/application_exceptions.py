class InvalidQuestionSourceData(Exception):
    def __init__(self, received):
        self.received = received

        super().__init__(
            "Invalid question source data received, "
            "expected a non-empty questions mapping. "
            f"Received: {received}"
        )