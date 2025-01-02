import logging
import os
import re
import subprocess
from collections import defaultdict
from collections.abc import Generator
from typing import Dict, List

from pyarchitecture import squire

LOGGER = logging.getLogger(__name__)


def parse_size(input_string: str) -> int:
    """Extracts size in bytes from a string.

    Args:
        input_string: Input string from diskutil output.

    Returns:
        int:
        Returns the size in bytes as an integer.
    """
    match = re.search(r"\((\d+) Bytes\)", input_string)
    return int(match.group(1)) if match else 0


def update_mountpoints(
    disks: List[Dict[str, str]], device_ids: defaultdict
) -> defaultdict:
    """Updates mount points for physical devices based on diskutil data.

    Args:
        disks: All disk info data as list.
        device_ids: Device IDs as default dict.

    Returns:
        defaultdict:
        Returns a defaultdict object with updated mountpoints as list.
    """
    for disk in disks:
        part_of_whole = disk.get("Part of Whole")
        apfs_store = disk.get("APFS Physical Store", "")
        mount_point = disk.get("Mount Point")
        read_only = "Yes" in disk.get("Volume Read-Only")
        if mount_point and not mount_point.startswith("/System/Volumes/"):
            if part_of_whole in device_ids:
                device_ids[part_of_whole].append(mount_point)
            else:
                for device_id in device_ids:
                    if apfs_store.startswith(device_id) and read_only:
                        device_ids[device_id].append(mount_point)
    for device_id, mountpoints in device_ids.items():
        if not mountpoints:
            device_ids[device_id] = []
    return device_ids


def parse_diskutil_output(stdout: str) -> List[Dict[str, str]]:
    """Parses `diskutil info -all` output into structured data.

    Args:
        stdout: Standard output from diskutil command.

    Returns:
        List[Dict[str, str]]:
        Returns a list of dictionaries with parsed drives' data.
    """
    disks = []
    disk_info = {}
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if line == "**********":
            disks.append(disk_info)
            disk_info = {}
        else:
            key, value = map(str.strip, line.split(":", 1))
            disk_info[key] = value
    return disks


def base_physical_device_id(disk_lib: str | os.PathLike) -> Generator[str]:
    """Get base physical device IDs for macOS devices.

    Args:
        disk_lib: Disk library path.

    Yields:
        str:
        Yields base physical device IDs.
    """
    result = subprocess.run([disk_lib, "list"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if (
            (line := line.strip())
            and "physical" in line
            and line.startswith("/dev/disk")
        ):
            yield line.split()[0]


def drive_info(disk_lib: str | os.PathLike) -> List[Dict[str, str | List[str]]]:
    """Get disks attached to macOS devices.

    Returns:
        List[Dict[str, str | List[str]]]:
        Returns disks information for macOS devices.
    """
    all_disk_info = subprocess.run(
        [disk_lib, "info", "-all"], capture_output=True, text=True
    )
    all_disks = parse_diskutil_output(all_disk_info.stdout)
    device_ids = defaultdict(list)
    physical_disks = []
    physical_disk_ids = list(base_physical_device_id(disk_lib))
    for disk in all_disks:
        if disk.get("Virtual") == "No" or disk.get("Device Node") in physical_disk_ids:
            physical_disks.append(
                {
                    "name": disk.get("Device / Media Name"),
                    "size": squire.size_converter(
                        parse_size(disk.get("Disk Size", ""))
                    ),
                    "device_id": disk.get("Device Identifier"),
                    "node": disk.get("Device Node"),
                }
            )
            # Instantiate default dict with keys as DeviceIDs and values as empty list
            _ = device_ids[disk["Device Identifier"]]
    mountpoints = update_mountpoints(all_disks, device_ids)
    for disk in physical_disks:
        disk["mountpoints"] = mountpoints[disk["device_id"]]
    return physical_disks
