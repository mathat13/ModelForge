from dataclasses import dataclass

from blueprint_forge.domain.question import Question
from blueprint_forge.domain.exceptions.domain_exceptions import (
    EmptyQuestionCollection,
    InvalidPrerequisites,
)

@dataclass(frozen=True)
class QuestionCollection:
    questions: list[Question]

    def __post_init__(self):
        # check for empty list
        if not self.questions:
            raise EmptyQuestionCollection()
        
        # construct dictionary of question_id: prerequisites
        dictionary = {
            question.id: question.prerequisites for question in self.questions
        }

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


        for question_id in dictionary:
            visit(question_id, set())
    

                
                
                    

