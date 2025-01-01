import logging
import os

from pyarchitecture import models
from pyarchitecture.cpu import main

LOGGER = logging.getLogger(__name__)


def _get_cpu_lib(user_input: str | os.PathLike) -> str:
    """Get the CPU library for the appropriate OS.

    Args:
        user_input: CPU library input by user.
    """
    cpu_lib = (
        user_input
        or os.environ.get("cpu_lib")
        or os.environ.get("CPU_LIB")
        or models.default_cpu_lib()[models.OPERATING_SYSTEM]
    )
    assert os.path.isfile(cpu_lib), f"CPU library {cpu_lib!r} doesn't exist"
    return cpu_lib


def get_cpu_name(cpu_lib: str | os.PathLike = None) -> str:
    """OS-agnostic function to get all CPUs connected to the host system.

    Args:
        cpu_lib: Custom CPU library path.

    Returns:
        List[Dict[str, str]]:
        Returns CPU name.
    """
    return main.get_name(_get_cpu_lib(cpu_lib))
