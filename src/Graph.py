from dataclasses import dataclass
from typing import List
from textwrap import wrap

from src import Question

DEFAULT_LABEL_WIDTH = 25

@dataclass
class GraphvizNode:
    id: str
    label: str
    shape: str
    peripheries: int | None = None

    def to_graphviz(self) -> str:
        attributes = [
            f'    label="{self.label}"',
            f'    shape={self.shape}',
        ]

        if self.peripheries is not None:
            attributes.append(
                f"    peripheries={self.peripheries}"
            )

        return (
            f"{self.id} [\n"
            + "\n".join(attributes)
            + "\n]"
        )

    @staticmethod
    def format_label(
        label: str,
        width: int = DEFAULT_LABEL_WIDTH,
    ) -> str:
        return "\\n".join(wrap(label, width=width))

    @staticmethod
    def determine_peripheries(question: Question) -> int | None:
        if question.knowledge is None and question.reasoning.status == "complete":
            return 2
        
        return None
    
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
            label=cls.format_label(label=question.question),                             
            shape=cls.determine_shape(question),
            peripheries=cls.determine_peripheries(question),
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
