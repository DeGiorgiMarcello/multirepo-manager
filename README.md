# Multirepository Manager
A CLI to perform simple git operation on multiple repository **at the same time**. The available commands are very limited, but they are the most common ones. The main goal of this project is to provide a simple way to manage multiple repositories at the same time, particularly useful if you are working on a multirepository project where all the involved distributions are installed in editable mode.

## Installation
To install the CLI, simply run the following command:

```
pip install multirepo-manager
```
## How to use it
1. Run the command you want to execute on all the repositories

Consider the following folder structure:

```
.
└── multirepo_project/
    ├── repo_1
    ├── repo_2
    └── repo_3
```
### Setup 
The first step is to set the path to the folder containing the involved repositories. 

This can be done either by:

1. Setting the env variable `REPOS_FOLDER`
1. Running the CLI command `multirepo set-folder /foo/bar/multirepo_project`

### Commands
Once the path is set, simply type `multirepo` on your command prompt to have a list of the available commands.


```> multirepo
Usage: multirepo [OPTIONS] COMMAND [ARGS]...

  CLI commands for simple git operation on multiple repositories in the same
  folder

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  fetch       Fetch all the repositories in the folder
  pull        Pull changes from all the repositories in the folder
  push        Push commits to all the repositories in the folder
  set-folder  Set the folder path containing the repositories
  switch      Switch to a branch (create it if does not exists) in all...
```


