import logging
import os
from typing import Dict

from pyarchitecture import config
from pyarchitecture.cpu import main

LOGGER = logging.getLogger(__name__)


def _get_cpu_lib(user_input: str | os.PathLike) -> str:
    """Get the CPU library for the appropriate OS.

    Args:
        user_input: CPU library input by user.
    """
    return (
        user_input
        or os.environ.get("cpu_lib")
        or os.environ.get("CPU_LIB")
        or config.default_cpu_lib()[config.OPERATING_SYSTEM]
    )


def get_cpu_info(cpu_lib: str | os.PathLike = None) -> str:
    """OS-agnostic function to get all CPUs connected to the host system.

    Args:
        cpu_lib: Custom CPU library path.

    Returns:
        str:
        Returns CPU name.
    """
    library_path = _get_cpu_lib(cpu_lib)
    if os.path.isfile(library_path):
        return main.get_name(library_path)
    LOGGER.error(f"CPU library {library_path!r} doesn't exist")
