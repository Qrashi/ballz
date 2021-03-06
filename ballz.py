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
    try:
        import platform

        if platform.system() == 'Windows':
            from ctypes import windll
            windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11), 7)
    except Exception as exc:  # skipcq: PYL-W0703 - Errors may cause the upper part to fail, but we don't care
        print(exc)
        print("! Failed to set console mode, some output may look weird. (windows problem)")

    config_file = pool.open("config.json")
    config = config_file.json

    if config["last_git_check"] == 0:
        git.update()
        # First time setup, install dependencies
        # Check for all dependencies
        try:
            import pygame
        except ModuleNotFoundError:
            # Install dependencies
            print("O Installing dependencies...")
            install = run(f"{sys.executable} -m pip install -r requirements.txt", shell=True, stdout=PIPE, stderr=PIPE)
            if install.returncode != 0:
                print(f"\r\033[K\r! Error; could not install required dependencies - return code {install.returncode}")
                print(f"! stdout: \n{install.stdout.decode('utf-8')}\n! stderr: \n{install.stderr.decode('utf-8')}")
                sys.exit()
            else:
                print(
                    "\r\033[K\rOK Installed dependencies")  # The \r\033[K\r means go to upper line, clear upper line and start writing
                # \r\033[K\r basically replaces the "Installing dependencies" with "Installed dependencies"
                os.execl(sys.executable, sys.executable, *sys.argv)  # Restart script

        # This will only get executed if the import of all dependencies succeeds
        config["last_git_check"] = datetime.now().timestamp()
        print("\r\033[K\rOK Installation complete")
        pool.sync()
        os.execl(sys.executable, sys.executable, *sys.argv)  # Restart script

    # Add potential "upgrade things" using config version here

    if "last_git_update" in config:
        del config["last_git_update"]
        config_file.save()

    if config["enable_git_auto_update"] and (datetime.now().timestamp() - config["last_git_check"]) > 60:
        # If git update enabled and time since last check less than 60 seconds
        # Fetch and pull git updates
        config["last_git_check"] = datetime.now().timestamp()
        config_file.save()
        if git.update():
            os.execl(sys.executable, sys.executable, *sys.argv)  # Restart script

    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    # Hide pygame message

    import sim
    sim.init()


if __name__ == "__main__":
    main()
