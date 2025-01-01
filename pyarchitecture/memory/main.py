import logging
import os
import subprocess
from typing import Dict

from pyarchitecture import models

LOGGER = logging.getLogger(__name__)


def get_memory_info_linux(mem_lib: str | os.PathLike):
    memory_info = {}
    with open(mem_lib) as f:
        for line in f:
            if line.startswith(('MemTotal', 'MemFree', 'MemAvailable', 'Buffers', 'Cached')):
                parts = line.split()
                memory_info[parts[0][:-1]] = int(parts[1])  # Convert the memory value to int (in kB)

    # Convert values to bytes (kB to bytes)
    total = memory_info.get('MemTotal', 0) * 1024
    free = memory_info.get('MemFree', 0) * 1024
    available = memory_info.get('MemAvailable', 0) * 1024
    used = total - free - available

    return {'total': total, 'free': free, 'used': used}


def get_memory_info_macos(mem_lib: str | os.PathLike):
    def get_sysctl_value(key):
        result = subprocess.run([mem_lib, key], capture_output=True, text=True)
        if result.stdout.strip():
            return int(result.stdout.split(":")[1].strip())
        return 0

    total = get_sysctl_value('hw.memsize')
    free = get_sysctl_value('vm.page_free_count') * get_sysctl_value('hw.pagesize')
    used = total - free

    return {'total': total, 'free': free, 'used': used}


def get_memory_info_windows(*args):
    import ctypes
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_uint),
            ("dwMemoryLoad", ctypes.c_uint),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("sullAvailExtendedVirtual", ctypes.c_ulonglong)
        ]

    # Initialize the MEMORYSTATUSEX structure
    memory_status = MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

    # Load the kernel32 DLL and call GlobalMemoryStatusEx
    memory_info = ctypes.windll.kernel32.GlobalMemoryStatusEx

    # Call GlobalMemoryStatusEx to fill in the memory_status structure
    if memory_info(ctypes.byref(memory_status)) == 0:
        LOGGER.error("Failed to retrieve memory status")
        return {}

    # Extract the values from the structure
    total = memory_status.ullTotalPhys  # Total physical memory (in bytes)
    available = memory_status.ullAvailPhys  # Available physical memory (in bytes)
    used = total - available  # Used memory (in bytes)

    # Optionally, you can also include virtual memory information
    virtual_total = memory_status.ullTotalVirtual
    virtual_available = memory_status.ullAvailVirtual

    return {
        'total': total,
        'available': available,
        'used': used,
        'virtual_total': virtual_total,
        'virtual_available': virtual_available,
    }


def get_mem_info(mem_lib: str | os.PathLike) -> Dict[str, int]:
    os_map = {
        models.OperatingSystem.darwin: get_memory_info_macos,
        models.OperatingSystem.linux: get_memory_info_linux,
        models.OperatingSystem.windows: get_memory_info_windows
    }
    try:
        return os_map[models.OPERATING_SYSTEM](mem_lib)
    except Exception as error:
        LOGGER.error(error)
