from typing import List
from dataclasses import dataclass        

from blueprint_forge.domain.knowledge import Knowledge
from blueprint_forge.domain.reasoning import Reasoning
from blueprint_forge.domain.exceptions.domain_exceptions import (
    InvalidQuestionID,
    InvalidQuestionState,
)

@dataclass
class Question:
    id: str
    question: str
    summary: str
    reasoning: Reasoning
    knowledge: Knowledge | None
    prerequisites: List[str]
        
    @classmethod
    def from_dict(cls, id: str, data: dict) -> "Question":

        # Validate id
        if not isinstance(id, str) or not id:
            raise InvalidQuestionID(received=id)

        # Must be present
        reasoning_data = data["reasoning"]
        # May not be present
        knowledge_data = data.get("knowledge")

        # Construct reasoning object
        reasoning = Reasoning(
                status=reasoning_data["status"],
                worksheet_path=reasoning_data.get("worksheet_path"),
            )
        
        # Construct knowledge object if present
        knowledge = (
            Knowledge(
                type=knowledge_data["type"],
                path=knowledge_data["path"],
                )
                if knowledge_data is not None
                else None
        )

        # reasoning.status -> knowledge state check
        if reasoning.status == "in_progress" and knowledge is not None:
            raise InvalidQuestionState(
                reason="in_progress reasoning cannot have knowledge",
                received={
                    "reasoning": reasoning,
                    "knowledge": knowledge,
                },
            )

        # Return question object
        return cls(
            id=id,
            question=data["question"],
            summary=data["summary"],
            reasoning=reasoning,
            knowledge=knowledge,
            prerequisites=data["prerequisites"],
        )