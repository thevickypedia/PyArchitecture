# PyArchitecture
PyArchitecture is a lightweight python module to get kernel information via OS specific CLI commands.

![Python][label-pyversion]

![Platform][label-platform]

[![pypi][label-actions-pypi]][gha_pypi]

[![Pypi][label-pypi]][pypi]
[![Pypi-format][label-pypi-format]][pypi-files]
[![Pypi-status][label-pypi-status]][pypi]

## Summary

PyArchitecture is designed to retrieve hard-to-find kernel information like CPU/GPU model name, physical disks,
and memory profiles without using any external dependencies.

> Although this project does not rely on external dependencies, it does use system tools, as outlined below.

| Library / Override       | Linux            | Darwin (macOS)              | Windows                                  |
|--------------------------|------------------|-----------------------------|------------------------------------------|
| **CPU**<br/>`cpu_lib`    | `/proc/cpuinfo`  | `/usr/sbin/sysctl`          | `C:\Windows\System32\wbem\wmic.exe`      |
| **PCI**<br/>`gpu_lib`    | `/usr/bin/lspci` | `/usr/sbin/system_profiler` | `C:\Windows\System32\wbem\wmic.exe`      |
| **Memory**<br/>`mem_lib` | `/proc/meminfo`  | `/usr/sbin/sysctl`          | N/A                                      |
| **Disk**<br/>`disk_lib`  | `/usr/bin/lsblk` | `/usr/sbin/diskutil`        | `C:\Program Files\PowerShell\7\pwsh.exe` |

## Installation

```shell
pip install PyArchitecture
```

## Usage

**Initiate - IDE**
```python
import pyarchitecture

if __name__ == '__main__':
    all_disks = pyarchitecture.disks.get_all_disks()
    print(all_disks)
    cpu_info = pyarchitecture.cpu.get_cpu_info()
    print(cpu_info)
    gpu_info = pyarchitecture.gpu.get_gpu_info()
    print(gpu_info)
    mem_info = pyarchitecture.memory.get_memory_info()
    print(mem_info)
```

**Initiate - CLI**
```shell
pyarchitecture all
```

> Use `pyarchitecture --help` for usage instructions.

## [Release Notes][release-notes]
**Requirement**
```shell
python -m pip install gitverse
```

**Usage**
```shell
gitverse-release reverse -f release_notes.rst -t 'Release Notes'
```

## Linting
`pre-commit` will ensure linting

**Requirement**
```shell
python -m pip install pre-commit
```

**Usage**
```shell
pre-commit run --all-files
```

## Pypi Package
[![pypi-module][label-pypi-package]][pypi-repo]

[https://pypi.org/project/PyArchitecture/][pypi]

## License & copyright

&copy; Vignesh Rao

Licensed under the [MIT License][license]

[license]: https://github.com/thevickypedia/PyArchitecture/blob/master/LICENSE
[label-pypi-package]: https://img.shields.io/badge/Pypi%20Package-PyArchitecture-blue?style=for-the-badge&logo=Python
[label-pyversion]: https://img.shields.io/badge/python-3.10%20%7C%203.11-blue
[label-platform]: https://img.shields.io/badge/Platform-Linux|macOS|Windows-1f425f.svg
[label-actions-pypi]: https://github.com/thevickypedia/PyArchitecture/actions/workflows/python-publish.yaml/badge.svg
[label-pypi]: https://img.shields.io/pypi/v/PyArchitecture
[label-pypi-format]: https://img.shields.io/pypi/format/PyArchitecture
[label-pypi-status]: https://img.shields.io/pypi/status/PyArchitecture
[gha_pypi]: https://github.com/thevickypedia/PyArchitecture/actions/workflows/python-publish.yaml
[pypi]: https://pypi.org/project/PyArchitecture
[pypi-files]: https://pypi.org/project/PyArchitecture/#files
[pypi-repo]: https://packaging.python.org/tutorials/packaging-projects/
[release-notes]: https://github.com/thevickypedia/PyArchitecture/blob/main/release_notes.rst
