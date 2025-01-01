# PhyDisk (Physical Disk)
PhyDisk is an ultra lightweight python module to get all physical disks connected to a host machine.

![Python][label-pyversion]

![Platform][label-platform]

[![pypi][label-actions-pypi]][gha_pypi]

[![Pypi][label-pypi]][pypi]
[![Pypi-format][label-pypi-format]][pypi-files]
[![Pypi-status][label-pypi-status]][pypi]

## Installation

```shell
pip install PhyDisk
```

## Usage

**Initiate - IDE**
```python
import phydisk

if __name__ == '__main__':
    all_disks = phydisk.get_all_disks()
    print(all_disks)
```

**Initiate - CLI**
```shell
phydisk print
```

> Use `phydisk --help` for usage instructions.

### Source Commands

**Linux**

```shell
/usr/bin/lsblk -o NAME,SIZE,TYPE,MODEL,MOUNTPOINT -J
```

**macOS**

```shell
/usr/sbin/diskutil info -all
```

**Windows**

```shell
C:\\Program Files\\PowerShell\\7\\pwsh.exe -Command
Get-PhysicalDisk | ForEach-Object {
    $disk = $_
    $partitions = Get-Partition -DiskNumber $disk.DeviceID
    $partitions | ForEach-Object {
        [PSCustomObject]@{
            DiskNumber = $disk.DeviceID
            Partition = $_.PartitionNumber
            DriveLetter = (Get-Volume -Partition $_).DriveLetter
            MountPoint = (Get-Volume -Partition $_).DriveLetter
        }
    }
}
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

[https://pypi.org/project/PhyDisk/][pypi]

## License & copyright

&copy; Vignesh Rao

Licensed under the [MIT License][license]

[license]: https://github.com/thevickypedia/PhyDisk/blob/master/LICENSE
[label-pypi-package]: https://img.shields.io/badge/Pypi%20Package-PhyDisk-blue?style=for-the-badge&logo=Python
[label-pyversion]: https://img.shields.io/badge/python-3.10%20%7C%203.11-blue
[label-platform]: https://img.shields.io/badge/Platform-Linux|macOS|Windows-1f425f.svg
[label-actions-pypi]: https://github.com/thevickypedia/PhyDisk/actions/workflows/python-publish.yaml/badge.svg
[label-pypi]: https://img.shields.io/pypi/v/PhyDisk
[label-pypi-format]: https://img.shields.io/pypi/format/PhyDisk
[label-pypi-status]: https://img.shields.io/pypi/status/PhyDisk
[gha_pypi]: https://github.com/thevickypedia/PhyDisk/actions/workflows/python-publish.yaml
[pypi]: https://pypi.org/project/PhyDisk
[pypi-files]: https://pypi.org/project/PhyDisk/#files
[pypi-repo]: https://packaging.python.org/tutorials/packaging-projects/
