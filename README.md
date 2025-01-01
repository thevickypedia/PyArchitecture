# PhyDisk (Physical Disk)

PhyDisk is an ultra lightweight python module to get all physical disks connected to a host machine.

## Installation

```shell
pip install PhyDisk
```

## Usage

```python
import phydisk

if __name__ == '__main__':
    all_disks = phydisk.get_all_disks()
    print(all_disks)
```

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
