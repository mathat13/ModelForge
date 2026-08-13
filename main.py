from pathlib import Path

from src import GraphvizApplication


def main():
    app = GraphvizApplication()

    app.generate(
        yaml_path=Path("data/source_map.yaml"),
        header_path=Path("templates/header.dot"),
        footer_path=Path("templates/footer.dot"),
        output_path=Path("output/reasoning_map.dot"),
    )


if __name__ == "__main__":
    main()