from typing import List

from pydantic import (
    BaseModel,
    ConfigDict
)

class QuestionDataBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class ReasoningData(QuestionDataBaseModel):
    status: str
    worksheet_path: str | None = None

class KnowledgeData(QuestionDataBaseModel):
    type: str
    path: str

class QuestionData(QuestionDataBaseModel):
    question: str
    summary: str
    reasoning: ReasoningData
    knowledge: KnowledgeData | None = None
    prerequisites: List[str]