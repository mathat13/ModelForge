from dataclasses import dataclass
from typing import List
from textwrap import wrap

from modelforge.domain.question import Question
from modelforge.representation.graphviz.node import GraphvizNode
from modelforge.representation.graphviz.edge import GraphvizEdge



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
