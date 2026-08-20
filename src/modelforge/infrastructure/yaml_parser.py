from pathlib import Path
import yaml

class YAMLParser:
    @staticmethod
    def parse(path: Path) -> dict:
        with open(path, 'r') as file:
                return yaml.safe_load(file)