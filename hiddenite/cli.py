import click
from hiddenite.core import process_files
from hiddenite.config import load_config, create_default_config

@click.group()
def cli():
    pass

@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option('--override', is_flag=True, help="Override and submit all files you find")
def run(directory, override):
    """
    Searches for files in a given directory, processes them.
    DIRECTORY must be a valid path. Use --override to process and submit all files found and ignore a check against the database.
    """
    db_config, api_url = load_config()
    print(f"Starting file search in '{directory}'")
    process_files(directory,db_config,api_url,override)
    print('dev')

@cli.command()
def init():
    """Initialize the configuration file"""
    create_default_config()

if __name__=="__main__":
    cli()
