from pathlib import Path

import typer

from question_translator.application.graphviz.application import GraphvizApplication

app = typer.Typer()


@app.callback()
def main():
    """Translate knowledge-base YAML into Graphviz representations."""
    pass

@app.command()
def generate(
    source: Path = typer.Argument(...),
):
    application = GraphvizApplication()
    
    application.generate(
        yaml_path=source,
        header_path=source,
        footer_path=source,
        output_path=source,
    )


if __name__ == "__main__":
    app()