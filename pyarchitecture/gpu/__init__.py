import logging
import os
from typing import Dict, List

from pyarchitecture import models
from pyarchitecture.gpu import main

LOGGER = logging.getLogger(__name__)


def _get_gpu_lib(user_input: str | os.PathLike) -> str:
    """Get the GPU library for the appropriate OS.

    Args:
        user_input: GPU library input by user.
    """
    return (
        user_input
        or os.environ.get("gpu_lib")
        or os.environ.get("GPU_LIB")
        or models.default_gpu_lib()[models.OPERATING_SYSTEM]
    )


def get_gpu_info(gpu_lib: str | os.PathLike = None) -> List[Dict[str, str]]:
    """OS-agnostic function to get all GPUs connected to the host system.

    Args:
        gpu_lib: Custom GPU library path.

    Returns:
        List[Dict[str, str]]:
        Returns the GPU model and vendor information as a list of key-value pairs.
    """
    library_path = _get_gpu_lib(gpu_lib)
    if os.path.isfile(library_path):
        return main.get_names(library_path)
    LOGGER.error(f"GPU library {library_path!r} doesn't exist")
