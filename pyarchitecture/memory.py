import psutil

from pyarchitecture import squire


def get_memory_info(raw: bool = False) -> dict[str, int | str]:
    """Get memory information for the host system.

    Returns:
        Dict[str, str]:
        Returns memory information.
    """
    if raw:
        return {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "used": psutil.virtual_memory().used,
            "free": psutil.virtual_memory().free,
        }
    return {
        "total": squire.size_converter(psutil.virtual_memory().total),
        "available": squire.size_converter(psutil.virtual_memory().available),
        "used": squire.size_converter(psutil.virtual_memory().used),
        "free": squire.size_converter(psutil.virtual_memory().free),
    }
