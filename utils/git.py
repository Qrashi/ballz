"""
A set of utilities for maintaining git repositories
"""
import os
import sys
from subprocess import run, PIPE


def fetch() -> bool:
    """
    Fetch updates
    :return: Whether a new version is available
    """
    print("\r\033[K\rO Fetching updates...", end="")
    fetch_process = run("git fetch origin", shell=True, stdout=PIPE, stderr=PIPE)
    if fetch_process.returncode != 0:
        print(f"\r\033[K\r! Error: Could not fetch git updates ({fetch_process.returncode})")
        print(f"! stdout: {fetch_process.stdout.decode('utf-8')}; stderr: {fetch_process.stderr.decode('utf-8')}")
    else:
        return "from" in fetch_process.stdout.decode('utf-8').lower() or "from" in fetch_process.stderr.decode('utf-8').lower()  # If message has content
    return False


def pull() -> bool:
    """
    Pull new updates from the repository
    :return: State of pull; successful or not
    """
    print("\r\033[K\rO Downloading updates...", end="")
    pull_process = run("git pull origin main", shell=True, stdout=PIPE, stderr=PIPE)
    if pull_process.returncode != 0:
        print(f"\r\033[K\r! Error: Could not pull git updates ({pull_process.returncode}")
        print(f"! stdout: ({pull_process.stdout.decode('utf-8')}); stderr: ({pull_process.stderr.decode('utf-8')})")
        return False
    if not pull_process.stdout.decode('utf-8').endswith("up to date.\n"):
        commit_process = run("git log -n 1 --pretty-format:\"%H\"", stdout=PIPE, stderr=PIPE, shell=True)
        if commit_process.returncode != 0:
            print("\r\033[K\rOK Updated to newest git version")
        else:
            print(f"\r\033[K\rOK Updated to commit {commit_process.stdout.decode('utf-8')}")
        return True
    return False


def update() -> bool:
    """
    Run full update cycle
    :return: if there has been an update
    """
    print("O Starting update", end="")
    if fetch():
        if not pull():
            print("\r\033[K\r! Update failed! (Nothing to update)")
            return False
        return True
    print("\r\033[K\rOK No updates found!")
    return False
