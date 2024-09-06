import click
from os import environ
from dotenv import load_dotenv
from pathlib import Path
import git

_ENV_FILE = Path(__file__).parents[1] / ".env"
load_dotenv(_ENV_FILE)


def get_repos_folders() -> list[Path]:
    """Returns a list of paths to the git repositories in the `REPOS_FOLDER`, if any.
    Returns:
        list[Path]: List of paths to the git repositories
    """
    repos_folder = environ.get("REPOS_FOLDER")
    if repos_folder:
        repos = [
            r for r in Path(repos_folder).iterdir() if r.is_dir() and is_git_repo(r)
        ]
        if not repos:
            click.secho(
                f"No git repositories found in the provided folder ({repos_folder}).",
                fg="red",
            )
            click.get_current_context().exit(2)
        return repos

    click.secho(
        "No folder path containing the repositories provided. Please use the 'set_folder' command to set it.",
        fg="red",
    )
    click.get_current_context().exit(2)


def is_git_repo(path: Path) -> bool:
    "Checks if a folder is a git repository."
    return (path / ".git").exists()


def iterate_and_apply(repos: list[Path], cmd: str):
    """Iterates over the repositories and applies the command `cmd` to each of them."""
    for repo in repos:
        click.echo(f"\n-- {repo} --\n")
        g = git.cmd.Git(repo)
        click.echo(getattr(g, cmd)())


@click.version_option(package_name="multirepo")
@click.group()
def cli():
    "CLI commands for simple git operation on multiple repositories in the same folder"


@click.command()
def fetch():
    "Fetch all the repositories in the folder"
    repos = get_repos_folders()
    iterate_and_apply(repos, cmd="fetch")


@click.command()
def push():
    "Push commits to all the repositories in the folder"
    repos = get_repos_folders()
    iterate_and_apply(repos, "push")


@click.command()
@click.argument("branch")
def switch(branch: str):
    "Switch to a branch (create it if does not exists) in all the repositories in the folder"
    repos = get_repos_folders()
    for repo in repos:
        click.echo(f"\n-- {repo} --\n")
        g = git.cmd.Git(repo)
        if branch in g.branch("--all").split():
            g.switch(branch)
            click.secho(f"Switched to branch {branch}", fg="green")
        else:
            if click.confirm(
                f"Branch {branch} not found in {repo}. Do you want to create it? (y/n)"
            ):
                g.checkout("-b", branch)
                click.secho(f"Branch {branch} created!", fg="green")


@click.command()
def pull():
    "Pull changes from all the repositories in the folder"
    repos_folder = get_repos_folders()
    iterate_and_apply(repos_folder, "pull")


@click.command()
@click.argument("path")
def set_folder(path: str):
    "Set the folder path containing the repositories"
    if environ.get("REPOS_FOLDER"):
        if not click.confirm(
            f"A folder path containing the repositories has already been set. Do you want to overwrite it? (y/n). The path set is '{path}'."
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
