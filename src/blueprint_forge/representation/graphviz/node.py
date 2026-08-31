from dataclasses import dataclass
from textwrap import wrap

from blueprint_forge.domain.question import Question

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

        else:
            if question.knowledge.type == "adr":
                return "box"

            elif question.knowledge.type == "classification":
                return "diamond"

            else:
                return "oval"

    @classmethod
    def from_question(cls, question: Question) -> "GraphvizNode":
        return cls(
            id=question.id,
            label=cls.format_label(label=question.question),                             
            shape=cls.determine_shape(question),
            peripheries=cls.determine_peripheries(question),
        )