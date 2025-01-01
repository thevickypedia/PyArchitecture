import json
import os
import subprocess
from typing import Dict, List


def drive_info(disk_lib: str | os.PathLike) -> List[Dict[str, str]]:
    """Get disks attached to Linux devices.

    Returns:
        List[Dict[str, str]]:
        Returns disks information for Linux distros.
    """
    # Using -d to list only physical disks, and filtering out loop devices
    result = subprocess.run(
        [disk_lib, "-o", "NAME,SIZE,TYPE,MODEL,MOUNTPOINT", "-J"],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    disks = []
    for device in data.get("blockdevices", []):
        if device["type"] == "disk":
            disk_info = {
                "device_id": device["name"],
                "size": device["size"],
                "name": device.get("model", "Unknown"),
                "mountpoints": [],
            }
            # Collect mount points from partitions
            if "children" in device:
                for partition in device["children"]:
                    if partition.get("mountpoint"):
                        disk_info["mountpoints"].append(partition["mountpoint"])
            if not disk_info["mountpoints"] and device.get("mountpoint"):
                if isinstance(device["mountpoint"], list):
                    disk_info["mountpoints"] = device["mountpoint"]
                else:
                    disk_info["mountpoints"] = [device["mountpoint"]]
            elif not disk_info["mountpoints"]:
                disk_info["mountpoints"] = ["Not Mounted"]
            disk_info["mountpoints"] = ", ".join(disk_info["mountpoints"])
            disks.append(disk_info)
    return disks
