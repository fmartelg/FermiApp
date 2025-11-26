"""Number formatting utilities for Fermi Calculator"""


def parse_number(s: str) -> float:
    """
    Parse a string with K/M/B suffixes into a float.
    
    Examples:
        parse_number("2.7M") -> 2700000.0
        parse_number("10K") -> 10000.0
        parse_number("1.5B") -> 1500000000.0
        parse_number("1000") -> 1000.0
    
    Args:
        s: String representation of a number (e.g., "2.7M", "10K", "1000")
    
    Returns:
        Float value
    
    Raises:
        ValueError: If string cannot be parsed
    """
    s = s.strip()
    
    if not s:
        raise ValueError("Empty string cannot be parsed as a number")
    
    # Define suffix multipliers
    suffixes = {
        'K': 1e3,
        'M': 1e6,
        'B': 1e9,
    }
    
    # Check if string ends with a suffix
    if s[-1].upper() in suffixes:
        suffix = s[-1].upper()
        number_part = s[:-1].strip()
        
        if not number_part:
            raise ValueError(f"Invalid number format: {s}")
        
        try:
            value = float(number_part)
            return value * suffixes[suffix]
        except ValueError:
            raise ValueError(f"Invalid number format: {s}")
    
    # No suffix, parse as plain number
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Invalid number format: {s}")


def format_number(n: float) -> str:
    """
    Format a number with appropriate K/M/B suffix.
    
    Examples:
        format_number(2700000) -> "2.70M"
        format_number(10000) -> "10.00K"
        format_number(100) -> "100"
    
    Args:
        n: Number to format
    
    Returns:
        Formatted string with suffix if appropriate
    """
    abs_n = abs(n)
    
    # Determine appropriate suffix
    if abs_n >= 1e9:
        return f"{n/1e9:.2f}B"
    elif abs_n >= 1e6:
        return f"{n/1e6:.2f}M"
    elif abs_n >= 1e3:
        return f"{n/1e3:.2f}K"
    else:
        # For small numbers, show without suffix
        if abs_n >= 10 or n == 0:
            return f"{n:.0f}"
        else:
            return f"{n:.2f}"