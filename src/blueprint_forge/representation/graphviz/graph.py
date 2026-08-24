from dataclasses import dataclass
from typing import List
from textwrap import wrap

from blueprint_forge.domain.question import Question
from blueprint_forge.representation.graphviz.node import GraphvizNode
from blueprint_forge.representation.graphviz.edge import GraphvizEdge



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
