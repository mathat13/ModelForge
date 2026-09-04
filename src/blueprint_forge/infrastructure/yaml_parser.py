from pathlib import Path
import yaml

from blueprint_forge.infrastructure.exceptions.infrastructure_exceptions import YAMLFileNotFound

class YAMLParser:
    @staticmethod
    def parse(path: Path) -> dict:
        try:
            with open(path, 'r') as file:
                    return yaml.safe_load(file)
        except FileNotFoundError:
            raise YAMLFileNotFound(path=path)

        