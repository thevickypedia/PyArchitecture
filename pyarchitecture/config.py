import platform
import shutil

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        """Custom StrEnum object for python3.10."""


OPERATING_SYSTEM = platform.system().lower()


class OperatingSystem(StrEnum):
    """Operating system names.

    >>> OperatingSystem

    """

    linux: str = "linux"
    darwin: str = "darwin"
    windows: str = "windows"


if OPERATING_SYSTEM not in (
    OperatingSystem.linux,
    OperatingSystem.darwin,
    OperatingSystem.windows,
):
    raise RuntimeError(
        f"{OPERATING_SYSTEM!r} is unsupported.\n\t"
        "Host machine should either be macOS, Windows or any Linux distros"
    )


def default_mem_lib():
    """Returns the default memory library dedicated to linux and macOS."""
    return dict(
        linux="/proc/meminfo",
        darwin=shutil.which("sysctl") or "/usr/sbin/sysctl",
        windows="",  # placeholder
    )


def default_disk_lib():
    """Returns the default disks' library dedicated to each supported operating system."""
    return dict(
        linux=shutil.which("lsblk") or "/usr/bin/lsblk",
        darwin=shutil.which("diskutil") or "/usr/sbin/diskutil",
        windows=shutil.which("pwsh") or "C:\\Program Files\\PowerShell\\7\\pwsh.exe",
    )


def default_cpu_lib():
    """Returns the default processor library dedicated to each supported operating system."""
    return dict(
        linux="/proc/cpuinfo",
        darwin=shutil.which("sysctl") or "/usr/sbin/sysctl",
        windows=shutil.which("wmic") or "C:\\Windows\\System32\\wbem\\wmic.exe",
    )


def default_gpu_lib():
    """Returns the default GPU library dedicated to each supported operating system."""
    return dict(
        linux=shutil.which("lspci") or "/usr/bin/lspci",
        darwin=shutil.which("system_profiler") or "/usr/sbin/system_profiler",
        windows=shutil.which("wmic") or "C:\\Windows\\System32\\wbem\\wmic.exe",
    )
