from pathlib import Path

import typer

from question_translator.application.graphviz.application import GraphvizApplication

app = typer.Typer()


@app.command()
def generate(
    source: Path,
):
    application = GraphvizApplication()

    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")
    
    #application.generate(
    #    yaml_path=source,
    #    # other paths/configuration will go here
    #)


def main() -> None:
    app()


if __name__ == "__main__":
    main()