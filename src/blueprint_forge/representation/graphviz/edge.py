from dataclasses import dataclass

@dataclass
class GraphvizEdge:
    start_node: str
    end_node: str

    def to_graphviz(self) -> str:
        return f"{self.start_node} -> {self.end_node}"