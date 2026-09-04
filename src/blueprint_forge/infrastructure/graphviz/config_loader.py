from pathlib import Path

from blueprint_forge.representation.graphviz.config import GraphvizConfig
from blueprint_forge.infrastructure.exceptions.infrastructure_exceptions import ConfigFileNotFound
class GraphvizConfigLoader:

    @staticmethod
    def load(
        header_path: Path,
        footer_path: Path,
    ) -> GraphvizConfig:

        try:
            header = header_path.read_text()
        except FileNotFoundError:
            raise ConfigFileNotFound(path=header_path)
    
        try:
            footer=footer_path.read_text()
        except FileNotFoundError:
            raise ConfigFileNotFound(path=footer_path)

        return GraphvizConfig(header=header,
                              footer=footer,
                              )