from pathlib import Path

class YAMLFileNotFound(Exception):
    path: Path
    def __init__(self, path: Path):
        self.path = path

        super().__init__(
            f"Attempt to load YAML file {path.as_posix()} failed, "
            f"Please check file exists."
        )

class ConfigFileNotFound(Exception):
    path: Path
    def __init__(self, path: Path):
        self.path = path

        super().__init__(
            f"Attempt to load config file {path.as_posix()} failed, "
            f"Please check file exists."
        )