import click
from pathlib import Path
from importer.process import process_json_file

@click.command(
    help="Process a JSON file of ChatGPT conversations and export each conversation to Markdown files."
)
@click.argument(
    "json_file",
    type=click.Path(exists=True, file_okay=True, path_type=Path),
    metavar="<JSON_FILE>",
)
@click.argument(
    "output_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    metavar="<OUTPUT_DIR>",
)
def cli(json_file: Path, output_dir: Path) -> None:
    """
    Processes a JSON file containing ChatGPT conversations and writes out Markdown
    files for each conversation to the specified output directory.

    The output directory will contain files in a structured tree:
      YYYY/MM/DD/YYYY-MM-DD Title.md

    Parameters:
      json_file: Path to the input JSON file containing the conversation list.
      output_dir: Base directory where the Markdown files will be saved.
    """
    process_json_file(json_file, output_dir)

if __name__ == "__main__":
    cli()
