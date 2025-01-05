import ctypes
import logging
from typing import Dict

LOGGER = logging.getLogger(__name__)


class MEMORYSTATUSEX(ctypes.Structure):
    """Structure for the GlobalMemoryStatusEx function overridden by ctypes.Structure.

    >>> MEMORYSTATUSEX

    """

    _fields_ = [
        ("dwLength", ctypes.c_uint),
        ("dwMemoryLoad", ctypes.c_uint),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


def get_memory_info(_: str) -> Dict[str, int]:
    """Get memory information for Windows OS.

    Returns:
        Dict[str, int]:
        Returns the memory information as key-value pairs.
    """
    # Initialize the MEMORYSTATUSEX structure
    memory_status = MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

    # Load the kernel32 DLL and call GlobalMemoryStatusEx
    memory_info = ctypes.windll.kernel32.GlobalMemoryStatusEx

    # Call GlobalMemoryStatusEx to fill in the memory_status structure
    if memory_info(ctypes.byref(memory_status)) == 0:
        LOGGER.error("Failed to retrieve memory status")
        return {}

    # Physical memory
    total = memory_status.ullTotalPhys
    available = memory_status.ullAvailPhys
    used = total - available

    # Virtual memory
    virtual_total = memory_status.ullTotalVirtual
    virtual_available = memory_status.ullAvailVirtual

    return {
        "total": total,
        "available": available,
        "used": used,
        "virtual_total": virtual_total,
        "virtual_available": virtual_available,
    }
