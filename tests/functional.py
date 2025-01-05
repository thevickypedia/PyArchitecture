import platform
from typing import Set, NoReturn

import pyarchitecture


def assert_disks(valid_keys: Set[str]) -> None | NoReturn:
    """Assert disks."""
    disk_info = pyarchitecture.disks.get_all_disks()
    assert disk_info
    for disk in disk_info:
        assert set(disk.keys()) == valid_keys
        # No assertion for values since they can be null in VMs


def assert_cpu() -> None | NoReturn:
    """Assert CPU output."""
    assert pyarchitecture.cpu.get_cpu_info()


def assert_memory(valid_keys: Set[str]) -> None | NoReturn:
    mem_info = pyarchitecture.memory.get_memory_info()
    assert set(mem_info.keys()) == valid_keys, f"{set(mem_info.keys())} != {valid_keys}"
    assert all(mem_info.values())


def main() -> None | NoReturn:
    """Main entrypoint."""
    system = platform.system().lower()
    disk_keys = {"name", "size", "device_id", "mountpoints"}
    memory_keys = {"total", "free", "used", "available"}
    if system == "darwin":
        disk_keys.add("node")
        memory_keys.update(("swap_total", "swap_used", "swap_free"))
    if system == "linux":
        memory_keys.update(("swap_total", "swap_used", "swap_free"))
    if system == "windows":
        # Windows doesn't have a distinction between free and available memory
        memory_keys.remove("free")
        memory_keys.update(("virtual_total", "virtual_available"))
    assert_disks(disk_keys)
    assert_cpu()
    assert_memory(memory_keys)


if __name__ == '__main__':
    main()
