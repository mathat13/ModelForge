from pathlib import Path
from question_translator.Graph import GraphvizConfig

class GraphvizConfigLoader:

    @staticmethod
    def load(
        header_path: Path,
        footer_path: Path,
    ) -> GraphvizConfig:

        return GraphvizConfig(
            header=header_path.read_text(),
            footer=footer_path.read_text(),
        )