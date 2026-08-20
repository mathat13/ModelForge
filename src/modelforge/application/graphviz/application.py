from pathlib import Path

from modelforge.infrastructure.yaml_parser import YAMLParser
from modelforge.infrastructure.graphviz.config_loader import GraphvizConfigLoader
from modelforge.infrastructure.file_writer import GraphvizFileWriter
from modelforge.application.graphviz.renderer import GraphvizRenderer
from modelforge.representation.graphviz.graph import GraphvizGraph
from modelforge.domain.question import Question


class GraphvizApplication:
    def __init__(self):
        self.renderer = GraphvizRenderer()

    def generate(
        self,
        yaml_path: Path,
        header_path: Path,
        footer_path: Path,
        output_path: Path,
    ):
        # Parse YAML to dict
        data = YAMLParser.parse(yaml_path)
        question_dict = data["questions"]

        # Construct domain objects
        questions = [
            Question.from_dict(
                id=question_id,
                data=question_data,
            )
            for question_id, question_data in question_dict.items()
        ]

        # Construct Graphviz representation
        graph = GraphvizGraph.from_questions(questions)

        # Load rendering configuration
        config = GraphvizConfigLoader.load(
            header_path=header_path,
            footer_path=footer_path,
        )

        # Render
        rendered_graph = self.renderer.render(
            graph=graph,
            config=config,
        )

        # Persist
        GraphvizFileWriter.write(
            output=rendered_graph,
            path=output_path,
        )
