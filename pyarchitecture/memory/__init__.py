import logging
import os
from typing import Dict

from pyarchitecture import models, squire
from pyarchitecture.memory import linux, macOS, windows

LOGGER = logging.getLogger(__name__)


def _get_mem_lib(user_input: str | os.PathLike) -> str:
    """Get the memory library for the appropriate OS.

    Args:
        user_input: Memory library input by user.
    """
    return (
        user_input
        or os.environ.get("mem_lib")
        or os.environ.get("MEM_LIB")
        or models.default_mem_lib()[models.OPERATING_SYSTEM]
        or __file__  # placeholder for windows
    )


def get_memory_info(
    mem_lib: str | os.PathLike = None, humanize: bool = True
) -> Dict[str, int | str]:
    """OS-agnostic function to get memory information.

    Args:
        mem_lib: Custom memory library path.
        humanize: Flag to return humanized memory info.

    Returns:
        Dict[str, int]:
        Returns the memory information as key-value pairs.
    """
    os_map = {
        models.OperatingSystem.darwin: macOS.get_memory_info,
        models.OperatingSystem.linux: linux.get_memory_info,
        models.OperatingSystem.windows: windows.get_memory_info,
    }
    library_path = _get_mem_lib(mem_lib)
    if os.path.isfile(library_path):
        raw_info = os_map[models.OPERATING_SYSTEM](library_path)
        if humanize:
            return {k: squire.size_converter(v) for k, v in raw_info.items()}
        return raw_info
    else:
        LOGGER.error(f"Memory library {library_path!r} doesn't exist")
