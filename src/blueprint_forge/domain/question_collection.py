from dataclasses import dataclass

from blueprint_forge.domain.question import Question
from blueprint_forge.domain.exceptions.domain_exceptions import (
    EmptyQuestionCollection,
    DuplicateQuestionID,
    InvalidPrerequisites,
)

@dataclass(frozen=True)
class QuestionCollection:
    questions: list[Question]

    def __post_init__(self):
        # check for empty list
        if not self.questions:
            raise EmptyQuestionCollection()

        # Construct dictionary of question.id: question.prerequisites 
        dictionary = {}

        for question in self.questions:
            # Check for duplicate question ids
            if question.id in dictionary:
                raise DuplicateQuestionID(question_id=question.id)

            dictionary[question.id] = question.prerequisites

        for question_id, prerequisites in dictionary.items():
            for prerequisite in prerequisites:

                # check for self-referential prerequisites
                if prerequisite == question_id:
                    raise InvalidPrerequisites(
                        reason=f"Self-referential prerequisite on question {id}.",
                    )

                # Check for unknown prerequisites
                if prerequisite not in dictionary:
                    raise InvalidPrerequisites(
                        reason=f"Prerequisite on question: {id} references non-existent question: {prerequisite}.",
                    )

        def visit(question_id, path):
            if question_id in path:
                raise InvalidPrerequisites(
                    reason=f"Prerequisite cycle detected on question: {question_id}."
                )

            path.add(question_id)

            for prerequisite in dictionary[question_id]:
                visit(prerequisite, path)

            path.remove(question_id)

        # Check for prerequisite cycles
        for question_id in dictionary:
            visit(question_id, set())
    

                
                
                    

