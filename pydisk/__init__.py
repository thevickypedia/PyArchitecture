import logging
import os
from typing import Dict, List

from . import linux, macOS, windows, models

version = "0.0.0-a1"

LOGGER = logging.getLogger(__name__)


def get_disk_lib(user_input: str | os.PathLike):
    disk_lib = (
            user_input or
            os.environ.get("disk_lib") or
            os.environ.get("DISK_LIB") or
            models.default_disk_lib()[models.OPERATING_SYSTEM]
    )
    assert os.path.isfile(disk_lib), f"Disk library {disk_lib!r} doesn't exist"
    return disk_lib


def get_all_disks(disk_lib: str | os.PathLike = None) -> List[Dict[str, str]]:
    """OS-agnostic function to get all disks connected to the host system."""
    os_map = {
        models.OperatingSystem.darwin: macOS.drive_info,
        models.OperatingSystem.linux: linux.drive_info,
        models.OperatingSystem.windows: windows.drive_info,
    }
    try:
        disk_lib = get_disk_lib(disk_lib)
        return os_map[models.OperatingSystem(models.OPERATING_SYSTEM)](disk_lib)
    except Exception as error:
        LOGGER.error(error)
