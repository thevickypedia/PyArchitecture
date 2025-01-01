import json
import logging
import os
import sys
import time
from typing import Dict, List

from . import linux, macOS, models, windows

version = "0.1.0"

LOGGER = logging.getLogger(__name__)


def get_disk_lib(user_input: str | os.PathLike) -> str:
    """Get the disk library for the appropriate OS.

    Args:
        user_input: Disk library input by user.
    """
    disk_lib = (
        user_input
        or os.environ.get("disk_lib")
        or os.environ.get("DISK_LIB")
        or models.default_disk_lib()[models.OPERATING_SYSTEM]
    )
    assert os.path.isfile(disk_lib), f"Disk library {disk_lib!r} doesn't exist"
    return disk_lib


def get_all_disks(disk_lib: str | os.PathLike = None) -> List[Dict[str, str]]:
    """OS-agnostic function to get all disks connected to the host system.

    Args:
        disk_lib: Custom disk library path.

    Returns:
        List[Dict[str, str]]:
        Returns a list of disk information.
    """
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
        return []


def commandline() -> None:
    """Starter function to invoke PhyDisk via CLI commands.

    **Flags**
        - ``--version | -V``: Prints the version.
        - ``--help | -H``: Prints the help section.
        - ``print``: Prints the disk information in terminal.
        - ``save``: Saves the disk information into a JSON file.
        - ``--filename``: Filename to store the disk information.
    """
    assert sys.argv[0].lower().endswith("phydisk"), "Invalid commandline trigger!!"

    print_ver = "--version" in sys.argv or "-V" in sys.argv
    get_help = "--help" in sys.argv or "-H" in sys.argv
    print_info = "print" in sys.argv
    save_info = "save" in sys.argv
    filename = None
    custom_filename = "--filename" in sys.argv
    if custom_filename:
        filename_idx = sys.argv.index("--filename") + 1
        try:
            filename = sys.argv[filename_idx]
            assert filename.endswith(".json")
        except IndexError:
            print("ERROR:\n\t--filename argument requires a value")
            sys.exit(1)
        except AssertionError:
            print("ERROR:\n\tfilename must be JSON")
            sys.exit(1)

    options = {
        "--version | -V": "Prints the version.",
        "--help | -H": "Prints the help section.",
        "print": "Prints the disk information in the terminal.",
        "save": "Saves the disk information into a JSON file.",
        "--filename": "Filename to store the disk information.",
    }
    # weird way to increase spacing to keep all values monotonic
    _longest_key = len(max(options.keys()))
    _pretext = "\n\t* "
    choices = _pretext + _pretext.join(
        f"{k} {'·' * (_longest_key - len(k) + 8)}→ {v}".expandtabs()
        for k, v in options.items()
    )

    if print_ver:
        print(f"PhyDisk {version}")
        sys.exit(0)

    if print_info:
        for disk in get_all_disks():
            print(disk)
        sys.exit(0)
    elif save_info:
        filename = filename or f"PhyDisk_{int(time.time())}.json"
        with open(filename, "w") as file:
            json.dump(get_all_disks(), file, indent=2)
        print(f"Physical disks' information has been stored in {filename!r}")
        sys.exit(0)
    else:
        get_help = True

    if get_help:
        print(
            f"\nUsage: phydisk [arbitrary-command]\n\nOptions (and corresponding behavior):{choices}"
        )
        sys.exit(0)
