import logging
import os
from typing import Dict, List

from pyarchitecture import config
from pyarchitecture.disks import linux, macOS, windows

LOGGER = logging.getLogger(__name__)


def _get_disk_lib(user_input: str | os.PathLike) -> str:
    """Get the disk library for the appropriate OS.

    Args:
        user_input: Disk library input by user.
    """
    return (
        user_input
        or os.environ.get("disk_lib")
        or os.environ.get("DISK_LIB")
        or config.default_disk_lib()[config.OPERATING_SYSTEM]
    )


def get_all_disks(disk_lib: str | os.PathLike = None) -> List[Dict[str, str]]:
    """OS-agnostic function to get all disks connected to the host system.

    Args:
        disk_lib: Custom disk library path.

    Returns:
        List[Dict[str, str]]:
        Returns a list of disk information.
    """
    library_path = _get_disk_lib(disk_lib)
    if os.path.isfile(library_path):
        os_map = {
            config.OperatingSystem.darwin: macOS.drive_info,
            config.OperatingSystem.linux: linux.drive_info,
            config.OperatingSystem.windows: windows.drive_info,
        }
        return os_map[config.OperatingSystem(config.OPERATING_SYSTEM)](library_path)
    LOGGER.error(f"Disk library {library_path!r} doesn't exist")
