import ctypes
import logging
from typing import Dict

LOGGER = logging.getLogger(__name__)


class MEMORYSTATUSEX(ctypes.Structure):
    """Structure for the GlobalMemoryStatusEx function overridden by ctypes.Structure.

    >>> MEMORYSTATUSEX

    References:
        https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/ns-sysinfoapi-memorystatusex
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
    # It is tied to the addressable memory space of your operating system and CPU architecture
    # It is not tied to the physical memory installed on your system
    # For example, a 64-bit processor can theoretically address 2^64 bytes of memory (16 exabytes)
    # Practical limits are imposed by the OS. So, Windows typically uses a 48-bit address space, corresponding to 128 TB
    virtual_total = memory_status.ullTotalVirtual
    virtual_available = memory_status.ullAvailVirtual

    return {
        "total": total,
        "available": available,
        "used": used,
        "virtual_total": virtual_total,
        "virtual_available": virtual_available,
    }
