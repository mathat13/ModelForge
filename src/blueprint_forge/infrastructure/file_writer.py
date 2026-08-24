from pathlib import Path

class GraphvizFileWriter:
    @staticmethod
    def write(output: str, path: Path) -> None:
        path.write_text(output)