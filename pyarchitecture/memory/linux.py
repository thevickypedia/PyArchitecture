import os
from typing import Dict


def get_memory_info(mem_lib: str | os.PathLike) -> Dict[str, int | str]:
    """Get memory information on Linux systems.

    Args:
        mem_lib: Memory library path.

    Returns:
        Dict[str, int]:
        Returns the memory information as key-value pairs.
    """
    memory_info = {}
    with open(mem_lib) as mem_file:
        for line in mem_file:
            if line.startswith(
                (
                    "MemTotal",
                    "MemFree",
                    "MemAvailable",
                    "SwapTotal",
                    "SwapFree",
                )
            ):
                parts = line.split()
                # Convert the memory value to int (in kB)
                memory_info[parts[0][:-1]] = int(parts[1])

    # Physical memory (kB to bytes)
    total = memory_info.get("MemTotal", 0) * 1024
    free = memory_info.get("MemFree", 0) * 1024
    available = memory_info.get("MemAvailable", 0) * 1024
    used = total - free - available

    # Swap memory (kB bytes)
    swap_total = memory_info.get("SwapTotal", 0) * 1024
    swap_free = memory_info.get("SwapFree", 0) * 1024
    swap_used = swap_total - swap_free

    return {
        "total": total,
        "free": free,
        "used": used,
        "swap_total": swap_total,
        "swap_used": swap_used,
        "swap_free": swap_free,
    }
