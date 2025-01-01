import os
import subprocess
from typing import Dict

from pyarchitecture import squire


def byte_value(text: str, key: str) -> int:
    """Converts the string value to bytes.

    Args:
        text: Text containing the value.
        key: Key to extract the value.

    Returns:
        int:
        Returns the value in bytes as an integer.
    """
    return squire.convert_to_bytes(text.split(f"{key} = ")[1].split()[0])


def get_sysctl_value(mem_lib: str | os.PathLike, key: str):
    """Get the value of the key from sysctl.

    Args:
        mem_lib: Memory library path.
        key: Key to extract the value.

    Returns:
        int:
        Returns the value of the key as an integer.
    """
    result = subprocess.run([mem_lib, key], capture_output=True, text=True)
    if text := result.stdout.strip():
        if key == "vm.swapusage":
            swap_usage = {}
            if "total" in text:
                swap_usage["swap_total"] = byte_value(text, "total")
            if "used" in text:
                swap_usage["swap_used"] = byte_value(text, "used")
            if "free" in text:
                swap_usage["swap_free"] = byte_value(text, "free")
            return swap_usage
        return int(text.split(":")[1].strip())
    return 0


def get_memory_info(mem_lib: str | os.PathLike) -> Dict[str, int | str]:
    """Get memory information on macOS systems.

    Args:
        mem_lib: Memory library path.

    Returns:
        Dict[str, int]:
        Returns the memory information as key-value pairs.
    """
    # Physical memory information
    total = get_sysctl_value(mem_lib, "hw.memsize")
    free = get_sysctl_value(mem_lib, "vm.page_free_count") * get_sysctl_value(
        mem_lib, "hw.pagesize"
    )
    used = total - free

    # Virtual memory information
    swap_info = get_sysctl_value(mem_lib, "vm.swapusage")

    return {
        **{
            "total": total,
            "free": free,
            "used": used,
        },
        **swap_info,
    }
