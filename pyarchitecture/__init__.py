import json
import sys
import time
from typing import Any, Dict, NoReturn

from pyarchitecture import cpu, disks, gpu, memory

version = "0.1.0a0"


def all_components() -> Dict[str, Any]:
    """Get all the architectural components of the system.

    Returns:
        Dict[str, Any]:
        Returns a dictionary of all the components' information.
    """
    return {
        "Disks": disks.get_all_disks(),
        "CPU": cpu.get_cpu_info(),
        "GPU": gpu.get_gpu_info(),
        "Memory": memory.get_memory_info(),
    }


def pprint(data: Any) -> NoReturn:
    """Pretty print the data and exit with return code 0."""
    print(json.dumps(data, indent=2))
    sys.exit(0)


def commandline() -> None:
    """Starter function to invoke PyArchitecture via CLI commands.

    **Flags**
        - ``--version | -V``: Prints the version.
        - ``--help | -H``: Prints the help section.
        - ``disk``: Prints the disk information in the terminal.
        - ``cpu``: Prints the CPU name in the terminal.
        - ``gpu``: Prints the GPU information in the terminal.
        - ``save``: Saves the chosen information into a JSON file.
        - ``--filename``: Filename to store the information.
    """
    assert (
        sys.argv[0].lower().endswith("pyarchitecture")
    ), "Invalid commandline trigger!!"

    print_ver = "--version" in sys.argv or "-V" in sys.argv
    get_help = "--help" in sys.argv or "-H" in sys.argv
    disk_info = "disk" in sys.argv
    cpu_info = "cpu" in sys.argv
    gpu_info = "gpu" in sys.argv
    mem_info = "memory" in sys.argv
    all_info = "all" in sys.argv
    save_info = "save" in sys.argv

    filename = None
    custom_filename = "--filename" in sys.argv
    if custom_filename:
        filename_idx = sys.argv.index("--filename") + 1
        try:
            filename = sys.argv[filename_idx]
            assert filename.endswith(".json")
        except IndexError:
            print("ERROR:\n\t--filename argument requires a value")
            sys.exit(1)
        except AssertionError:
            print("ERROR:\n\tfilename must be JSON")
            sys.exit(1)

    options = {
        "--version | -V": "Prints the version.",
        "--help | -H": "Prints the help section.",
        "all": "Prints the entire system information in the terminal.",
        "disk": "Prints the disk information in the terminal.",
        "cpu": "Prints the CPU name in the terminal.",
        "gpu": "Prints the GPU information in the terminal.",
        "memory": "Prints the RAM/memory information in the terminal.",
        "save": "Saves the chosen information into a JSON file.",
        "--filename": "Filename to store the information.",
    }
    # weird way to increase spacing to keep all values monotonic
    _longest_key = len(max(options.keys()))
    _pretext = "\n\t* "
    choices = _pretext + _pretext.join(
        f"{k} {'·' * (_longest_key - len(k) + 8)}→ {v}".expandtabs()
        for k, v in options.items()
    )

    if print_ver:
        print(f"PyArchitecture {version}")
        sys.exit(0)

    if disk_info and not save_info:
        pprint(disks.get_all_disks())
    if cpu_info and not save_info:
        pprint(cpu.get_cpu_info())
    if gpu_info and not save_info:
        pprint(gpu.get_gpu_info())
    if mem_info and not save_info:
        pprint(memory.get_memory_info())
    if all_info and not save_info:
        pprint(all_components())

    if not any([disk_info, cpu_info, gpu_info, all_info]):
        save_info = False

    if save_info:
        filename = filename or f"PyArchitecture_{int(time.time())}.json"
        if all_info:
            data = all_components()
        else:
            data = {}
            if cpu_info:
                data["CPU"] = cpu.get_cpu_info()
            if gpu_info:
                data["GPU"] = gpu.get_gpu_info()
            if disk_info:
                data["Disks"] = disks.get_all_disks()
            if mem_info:
                data["Memory"] = memory.get_memory_info()

        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=2)
        print(f"Architecture information has been stored in {filename!r}")
        sys.exit(0)
    else:
        get_help = True

    if get_help:
        print(
            f"\nUsage: pyarchitecture [arbitrary-command]\n\nOptions (and corresponding behavior):{choices}"
        )
        sys.exit(0)
