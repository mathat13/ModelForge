from dataclasses import dataclass
from typing import List

from src import Question

@dataclass
class GraphvizNode:
    id: str
    label: str
    shape: str

    def to_graphviz(self) -> str:
        return (f'{self.id} [\n'
            f'    label="{self.label}"\n'
            f'    shape={self.shape}\n'
            f']'
        )

    @staticmethod
    def determine_shape(question: Question) -> str:
        if question.knowledge is None:
            return "oval"

        if question.knowledge.type == "adr":
            return "box"

        if question.knowledge.type == "classification":
            return "diamond"

        return "oval"

    @classmethod
    def from_question(cls, question: Question) -> "GraphvizNode":
        return cls(
            id=question.id,
            label=question.question,
            shape=cls.determine_shape(question),
        )

@dataclass
class GraphvizEdge:
    start_node: str
    end_node: str

    def to_graphviz(self) -> str:
        return f"{self.start_node} -> {self.end_node}"

@dataclass
class GraphvizConfig:
    header: str
    footer: str

@dataclass
class GraphvizGraph:
    nodes: List[GraphvizNode]
    edges: List[GraphvizEdge]

    @classmethod
    def from_questions(cls, questions: List[Question]) -> "GraphvizGraph":
            nodes = [
                GraphvizNode.from_question(question)
                for question in questions
            ]

            edges = [
                GraphvizEdge(
                    start_node=prerequisite,
                    end_node=question.id,
                )
                for question in questions
                for prerequisite in question.prerequisites
            ]

            return cls(
                 nodes=nodes,
                 edges=edges,
            )
