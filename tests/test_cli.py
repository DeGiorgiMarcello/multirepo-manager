from src.cli import get_repos_folders, iterate_and_apply, is_git_repo, cli
from click.testing import CliRunner
from unittest.mock import Mock
from pathlib import Path


def test_get_repos_folders_no_repos(monkeypatch):
    click_mock = Mock()
    monkeypatch.setattr("src.cli.click", click_mock)
    monkeypatch.delenv("REPOS_FOLDER")
    get_repos_folders()
    click_mock.secho.assert_called_once_with(
        "No folder path containing the repositories provided. Please use the 'set_folder' command to set it.",
        fg="red",
    )


def test_get_repos_folders_no_git_repos(monkeypatch, tmp_path):
    click_mock = Mock()
    monkeypatch.setattr("src.cli.click", click_mock)
    monkeypatch.setenv("REPOS_FOLDER", tmp_path)
    get_repos_folders()
    click_mock.secho.assert_called_once_with(
        f"No git repositories found in the provided folder ({tmp_path}).",
        fg="red",
    )


def test_get_repos_folders(monkeypatch):
    expected = [Path("A"), Path("B")]
    monkeypatch.setenv("REPOS_FOLDER", "tests/repos")
    monkeypatch.setattr("src.cli.Path.iterdir", lambda x: expected)
    monkeypatch.setattr("src.cli.Path.is_dir", lambda x: True)
    monkeypatch.setattr("src.cli.is_git_repo", lambda x: True)
    res = get_repos_folders()

    assert res == expected


def test_is_git_repo(tmp_path):
    (tmp_path / ".git").touch()

    assert not is_git_repo(Path("tests/repos/A"))
    assert is_git_repo(tmp_path)


def test_set_folder(monkeypatch, tmp_path):
    monkeypatch.delenv("REPOS_FOLDER")
    monkeypatch.setattr("src.cli._ENV_FILE", tmp_path / ".env")
    runner = CliRunner()
    result = runner.invoke(cli, ["set-folder", "tests/repos"])
    assert result.exit_code == 0
    assert "Folder path set successfully! (tests/repos)" in result.output


def test_set_folder_already_set(monkeypatch, tmp_path):
    monkeypatch.setenv("REPOS_FOLDER", "tests/repos")

    runner = CliRunner()
    result = runner.invoke(cli, ["set-folder", "tests/repos"])
    assert result.exit_code == 0
    assert "A folder path containing the repositories" in result.output
