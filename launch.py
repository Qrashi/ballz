"""
A script to install all dependencies, update the project and launch the simulation
"""
import os
import sys
from datetime import datetime
from subprocess import run, PIPE

from utils import git
from utils import pool


def main():
    """
    Launch the simulation
    :return:
    """
    config = pool.open("config.json").json

    if config["last_git_check"] == 0:
        git.update()
        # First time setup, install dependencies
        # Check for all dependencies
        try:
            import pygame
        except ModuleNotFoundError:
            # Install dependencies
            print("O Installing dependencies...")
            install = run("python -m pip install -r requirements.txt", shell=True, stdout=PIPE, stderr=PIPE)
            if install.returncode != 0:
                print(f"\r\033[K\r! Error; could not install required dependencies - return code {install.returncode}")
                print(f"! stdout: \n{install.stdout.decode('utf-8')}\n! stderr: \n{install.stderr.decode('utf-8')}")
                sys.exit()
            else:
                print(
                    "\r\033[K\r✓ Installed dependencies")  # The \r\033[K\r means go to upper line, clear upper line and start writing
                # \r\033[K\r basically replaces the "Installing dependencies" with "Installed dependencies"
                os.execl(sys.executable, sys.executable, *sys.argv)  # Restart script

        # This will only get executed if the import of all dependencies succeeds
        config["last_git_check"] = datetime.now().timestamp()
        print("\r\033[K\r✓ Installation complete")
        pool.sync()
        os.execl(sys.executable, sys.executable, *sys.argv)  # Restart script

    # Add potential "upgrade things" using config version here

    if config["enable_git_auto_update"] and (datetime.now().timestamp() - config["last_git_check"]) > 60:
        # If git update enabled and time since last check less than 60 seconds
        # Fetch and pull git updates
        git.update()
        config["last_git_update"] = datetime.now().timestamp()

    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    # Hide pygame message

    import sim
    sim.init()


if __name__ == "__main__":
    main()
