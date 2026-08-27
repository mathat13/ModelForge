from dataclasses import dataclass

@dataclass
class Reasoning:
    status: str
    worksheet_path: str | None