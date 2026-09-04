from pathlib import Path

from blueprint_forge.infrastructure.yaml_parser import YAMLParser
from blueprint_forge.infrastructure.file_writer import GraphvizFileWriter
from blueprint_forge.infrastructure.graphviz.config_loader import GraphvizConfigLoader
from blueprint_forge.representation.graphviz.graph import GraphvizGraph
from blueprint_forge.domain.question import Question
from blueprint_forge.domain.question_collection import QuestionCollection
from blueprint_forge.application.graphviz.renderer import GraphvizRenderer
from blueprint_forge.application.inputs import QuestionData

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

        questions = []

        for question_id, question_data in question_dict.items():
            
            # Validate question_data
            validated_data = QuestionData.model_validate(question_data)

            # Request domain object instantiation and append to list if successful
            questions.append(
                Question.from_dict(
                    id=question_id,
                    data=validated_data.model_dump(),
                )
            )

        # Validate question relationships
        question_collection = QuestionCollection(questions=questions)
            
        # Construct Graphviz representation
        graph = GraphvizGraph.from_question_collection(collection=question_collection)

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
