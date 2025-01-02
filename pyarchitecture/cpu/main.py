import logging
import os
import subprocess

from pyarchitecture.cpu import config

LOGGER = logging.getLogger(__name__)


def _darwin(cpu_lib: str | os.PathLike) -> str:
    """Get processor information for macOS."""
    command = [cpu_lib, "-n", "machdep.cpu.brand_string"]
    return subprocess.check_output(command).decode().strip()


def _linux(cpu_lib: str | os.PathLike) -> str:
    """Get processor information for Linux."""
    with open(cpu_lib) as file:
        for line in file:
            if "model name" in line:
                return line.split(":")[1].strip()


def _windows(cpu_lib: str | os.PathLike) -> str:
    """Get processor information for Windows."""
    command = f"{cpu_lib} cpu get name"
    output = subprocess.check_output(command, shell=True).decode()
    return output.strip().split("\n")[1]


def get_name(cpu_lib: str | os.PathLike) -> str | None:
    """Get processor information for the host operating system.

    Returns:
        str:
        Returns the processor information as a string.
    """
    os_map = {
        config.OperatingSystem.darwin: _darwin,
        config.OperatingSystem.linux: _linux,
        config.OperatingSystem.windows: _windows,
    }
    try:
        return os_map[config.OPERATING_SYSTEM](cpu_lib)
    except Exception as error:
        LOGGER.error(error)
