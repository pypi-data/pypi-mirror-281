"""Python Integration, Delivery & Deployment."""

__version__ = "0.0.1"

import os
import sys
from pathlib import Path

import env
from rwx import fs
from rwx.log import stream as log

import spcd
from spcd import cmd
from spcd.project import Project
from spcd.projects import Projects

COMMANDS_PREFIX = "spcd-"

projects = Projects()
project = Project(projects)


def browse(root: str) -> None:
    paths = []
    for directory, _, files in os.walk(root):
        for file in files:
            absolute_path = Path(directory) / file
            relative_path = os.path.relpath(absolute_path, start=root)
            paths.append(relative_path)
    frame(root)
    for path in sorted(paths):
        log.info(path)
    shut(root)


def cat(file: str) -> None:
    frame(file)
    log.info(fs.read_file_text(file).rstrip())
    shut(file)


def install_commands(path: str) -> None:
    step("Install commands")
    user = Path("/usr/local/bin")
    for command in [
        "browse-workspace",
        "build-project",
        "clone-branch",
        "list-environment",
        "synchronize",
    ]:
        log.info(command)
        (user / f"{COMMANDS_PREFIX}{command}").symlink_to(path)


def main(main: str) -> None:
    path, *arguments = sys.argv
    name = Path(path).name
    if name == "__main__.py":
        spcd.set_ssh(*arguments)
        spcd.install_commands(main)
    else:
        function = getattr(cmd, name.replace("-", "_"))
        function(*arguments)


def set_ssh(*arguments: list[str]) -> None:
    step("Set SSH")
    #
    ssh_key, ssh_hosts = arguments
    #
    ssh_type = "ed25519"
    #
    home = Path("~").expanduser()
    #
    ssh = home / ".ssh"
    ssh.mkdir(exist_ok=True, parents=True)
    ssh.chmod(0o700)
    #
    key = ssh / f"id_{ssh_type}"
    if ssh_key:
        fs.write(key, ssh_key)
        key.chmod(0o400)
    #
    known = ssh / "known_hosts"
    if ssh_hosts:
        fs.write(known, ssh_hosts)
        known.chmod(0o400)
    #
    browse(ssh)
    cat(known)


def frame(text: str) -> None:
    log.info(f"{env.SPCD_OPEN}{text}")


def shut(text: str) -> None:
    log.info(f"{env.SPCD_SHUT}{text}")


def split() -> None:
    log.info(env.SPCD_SPLT)


def step(text: str) -> None:
    env.SPCD_STEP += 1
    log.info(env.SPCD_DOWN)
    log.info(f"{env.SPCD_VERT} {env.SPCD_STEP} {text}")
    log.info(env.SPCD___UP)
