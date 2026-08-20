from typing import List
from dataclasses import dataclass        

from modelforge.domain.knowledge import Knowledge
from modelforge.domain.reasoning import Reasoning

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
        reasoning_data = data["reasoning"]
        knowledge_data = data.get("knowledge")

        return cls(
            id=id,
            question=data["question"],
            summary=data["summary"],
            reasoning=Reasoning(
                status=reasoning_data["status"],
                worksheet_path=reasoning_data.get("worksheet_path"),
            ),
            knowledge=(
                Knowledge(
                    type=knowledge_data["type"],
                    path=knowledge_data["path"],
                )
                if knowledge_data is not None
                else None
            ),
            prerequisites=data["prerequisites"],
        )