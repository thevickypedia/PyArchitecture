import json
import sys
import time

from pyarchitecture import disks

version = "0.0.0-a0"


def commandline() -> None:
    """Starter function to invoke PyArchitecture via CLI commands.

    **Flags**
        - ``--version | -V``: Prints the version.
        - ``--help | -H``: Prints the help section.
        - ``print``: Prints the disk information in terminal.
        - ``save``: Saves the disk information into a JSON file.
        - ``--filename``: Filename to store the disk information.
    """
    assert sys.argv[0].lower().endswith("pyarchitecture"), "Invalid commandline trigger!!"

    print_ver = "--version" in sys.argv or "-V" in sys.argv
    get_help = "--help" in sys.argv or "-H" in sys.argv
    disk_info = "disk" in sys.argv
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
        "disk": "Prints the disk information in the terminal.",
        "save": "Saves the disk information into a JSON file.",
        "--filename": "Filename to store the disk information.",
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

    if disk_info:
        for disk in disks.get_all_disks():
            print(disk)
        sys.exit(0)
    elif save_info:
        filename = filename or f"PyArchitecture_{int(time.time())}.json"
        with open(filename, "w") as file:
            json.dump(disks.get_all_disks(), file, indent=2)
        print(f"Physical disks' information has been stored in {filename!r}")
        sys.exit(0)
    else:
        get_help = True

    if get_help:
        print(
            f"\nUsage: pyarchitecture [arbitrary-command]\n\nOptions (and corresponding behavior):{choices}"
        )
        sys.exit(0)
