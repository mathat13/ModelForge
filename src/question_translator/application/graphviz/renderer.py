from dataclasses import dataclass

from question_translator.representation.graphviz.graph import GraphvizGraph
from question_translator.representation.graphviz.config import GraphvizConfig

class GraphvizRenderer:
    def render(
        self,
        graph: GraphvizGraph,
        config: GraphvizConfig,
    ) -> str:
        rendered_graph = []

        rendered_graph.append(config.header)

        for node in graph.nodes:
            rendered_graph.append(node.to_graphviz())

        for edge in graph.edges:
            rendered_graph.append(edge.to_graphviz())

        rendered_graph.append(config.footer)

        return "\n".join(rendered_graph)
