import subprocess


def run_subprocess(command):
    """Run a subprocess command and handle errors.

    Args:
        command (list): The command to run as a subprocess.
    """
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a subprocess: {e}")
        raise
