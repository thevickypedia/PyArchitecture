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
    with open(mem_lib) as f:
        for line in f:
            if line.startswith(
                ("MemTotal", "MemFree", "MemAvailable", "Buffers", "Cached")
            ):
                parts = line.split()
                memory_info[parts[0][:-1]] = int(
                    parts[1]
                )  # Convert the memory value to int (in kB)

    # Convert values to bytes (kB to bytes)
    total = memory_info.get("MemTotal", 0) * 1024
    free = memory_info.get("MemFree", 0) * 1024
    available = memory_info.get("MemAvailable", 0) * 1024
    used = total - free - available

    return {"total": total, "free": free, "used": used}
