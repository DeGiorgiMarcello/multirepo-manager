import click
from os import environ
from dotenv import load_dotenv
from pathlib import Path
import git

_ENV_FILE = Path(__file__).parents[1] / ".env"
load_dotenv(_ENV_FILE)


def get_repos_folder() -> Path:
    repos_folder = environ.get("REPOS_FOLDER")
    if repos_folder:
        return Path(repos_folder)
    click.secho(
        "No folder path containing the repositories provided. Please use the 'set_folder' command to set it.",
        fg="red",
    )
    click.get_current_context().exit(2)


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def iterate_over(repos_folder: Path, cmd: str):
    repos = [r for r in repos_folder.iterdir() if r.is_dir() and is_git_repo(r)]
    if not repos:
        click.secho(
            f"No git repositories found in the provided folder ({repos_folder}).",
            fg="red",
        )
    for repo in repos:
        click.echo(f"\n-- {repo} --\n")
        g = git.cmd.Git(repo)
        click.echo(getattr(g, cmd)())


@click.group()
def cli(): ...


@click.command()
def fetch():
    repos_folder = get_repos_folder()
    iterate_over(repos_folder, cmd="fetch")


@click.command()
def push():
    repos_folder = get_repos_folder()


@click.command()
def switch():
    repos_folder = get_repos_folder()


@click.command()
def pull():
    repos_folder = get_repos_folder()


@click.command()
@click.argument("path")
def set_folder(path: str):
    if environ.get("REPOS_FOLDER"):
        if not click.confirm(
            f"A folder path containing the repositories has already been set. Do you want to overwrite it? (y/n). The set path is '{path}'."
        ):
            click.get_current_context().exit(0)

    with _ENV_FILE.open("w") as f:
        f.write(f"REPOS_FOLDER={path}")
    click.secho(f"Folder path set successfully! ({path})", fg="green")


cli.add_command(fetch)
cli.add_command(push)
cli.add_command(switch)
cli.add_command(pull)
cli.add_command(set_folder)
