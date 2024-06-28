import os
from pathlib import Path

from rwx import ps
from rwx.log import stream as log

from spcd import browse, project, projects, split


def spcd_browse_workspace() -> None:
    browse(project.root)


def spcd_build_project() -> None:
    for extension in ["py", "sh"]:
        path = Path(project.root) / f"build.{extension}"
        if path.exists():
            ps.run(path)
            break
    else:
        pass


def spcd_clone_branch() -> None:
    log.info(projects)
    split()
    log.info(project)
    split()
    log.info(f"""\
{project.url}
↓
""")
    ps.run(
        "git",
        "clone",
        "--branch",
        project.branch,
        "--",
        project.url,
        project.root,
    )


def spcd_list_environment() -> None:
    for variable, value in sorted(projects.environment.items()):
        log.info(f"{variable} = {value}")


def spcd_synchronize() -> None:
    host = "rwx.work"
    source = "out"
    user = "cd"
    #
    root = Path(os.sep) / user / project.branch / projects.group / project.name
    #
    target = f"{user}@{host}:{root}"
    ps.run(
        "rsync",
        "--archive",
        "--delete-before",
        "--verbose",
        f"{source}/",
        f"{target}/",
        "--dry-run",
    )
