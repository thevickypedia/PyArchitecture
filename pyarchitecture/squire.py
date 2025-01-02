import math


def format_nos(input_: float) -> int | float:
    """Removes ``.0`` float values.

    Args:
        input_: Strings or integers with ``.0`` at the end.

    Returns:
        int | float:
        Int if found, else returns the received float value.
    """
    return int(input_) if isinstance(input_, float) and input_.is_integer() else input_


def size_converter(byte_size: int | float) -> str:
    """Gets the current memory consumed and converts it to human friendly format.

    Args:
        byte_size: Receives byte size as argument.

    Returns:
        str:
        Converted human-readable size.
    """
    if byte_size:
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        index = int(math.floor(math.log(byte_size, 1024)))
        return (
            f"{format_nos(round(byte_size / pow(1024, index), 2))} {size_name[index]}"
        )
    return "0 B"


def convert_to_bytes(size_str: str) -> int:
    """Convert a size string to bytes.

    Args:
        size_str (str): Size string to convert to bytes.

    Returns:
        int:
        Size in bytes.
    """
    # Dictionary to map size units to their respective byte multipliers
    units = {
        "B": 1,  # Bytes
        "K": 1024,  # Kilobytes
        "M": 1024 * 1024,  # Megabytes
        "G": 1024 * 1024 * 1024,  # Gigabytes
        "T": 1024 * 1024 * 1024 * 1024,  # Terabytes
        "P": 1024 * 1024 * 1024 * 1024 * 1024,  # Petabytes
        "E": 1024 * 1024 * 1024 * 1024 * 1024 * 1024,  # Exabytes
    }

    # Strip extra spaces and make the string uppercase
    size_str = size_str.strip().upper()

    # Find the last character, which should indicate the unit (B, K, M, G, T, P, E)
    if size_str[-1] in units:
        # Extract the numeric value and unit
        # everything except the last character (unit)
        numeric_part = size_str[:-1].strip()
        # the last character (unit)
        unit_part = size_str[-1]

        # Ensure the numeric part is a valid number
        try:
            numeric_value = float(numeric_part)
        except ValueError:
            raise ValueError("Invalid numeric value.")

        # Convert the size to bytes using the multiplier from the dictionary
        return int(numeric_value * units[unit_part])

    else:
        raise ValueError("Invalid size unit. Supported units are B, K, M, G, T, P, E.")
