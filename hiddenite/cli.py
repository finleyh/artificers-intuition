import click
from hiddenite.core import process_files
from hiddenite.config import load_config, create_default_config

@click.group()
def cli():
    pass

@cli.command()
@click.argument("directory", type=click.Path(exists=True))
def run(directory):
    db_config, api_url = load_config()
    print(f"Starting file search in '{directory}'")
    process_files(directory,db_config,api_url)

@cli.command()
def init():
    """Initialize the configuration file"""
    create_default_config()

if __name__=="__main__":
    cli()
