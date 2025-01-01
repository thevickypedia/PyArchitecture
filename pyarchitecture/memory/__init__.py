import logging
import os
from typing import Dict, List

from pyarchitecture import models
from pyarchitecture.memory import main

LOGGER = logging.getLogger(__name__)


def _get_mem_lib(user_input: str | os.PathLike) -> str:
    """Get the memory library for the appropriate OS.

    Args:
        user_input: Memory library input by user.
    """
    mem_lib = (
        user_input
        or os.environ.get("mem_lib")
        or os.environ.get("MEM_LIB")
        or models.default_mem_lib()[models.OPERATING_SYSTEM]
    )
    assert os.path.isfile(mem_lib), f"Memory library {mem_lib!r} doesn't exist" if mem_lib else None
    return mem_lib


def get_memory_info(mem_lib: str | os.PathLike = None) -> Dict[str, int]:
    """OS-agnostic function to get memory information.

    Args:
        mem_lib: Custom memory library path.

    Returns:
        List[Dict[str, str]]:
        Returns the memory model and vendor information as a list of key-value pairs.
    """
    return main.get_mem_info(_get_mem_lib(mem_lib))
