import re
from typing import Set

# Valid IP address statuses
VALID_STATUSES: Set[str] = {"Active", "Inactive", "Reserved"}


def validate_ip(ip: str) -> bool:
    """Validate an IPv4 address string."""
    pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if not re.match(pattern, ip.strip()):
        return False
    return all(0 <= int(p) <= 255 for p in ip.strip().split("."))


def validate_subnet(subnet: str) -> bool:
    """Validate subnet — accepts CIDR (0-32) or dotted netmask notation."""
    subnet = subnet.strip()
    # CIDR prefix
    try:
        val = int(subnet)
        return 0 <= val <= 32
    except ValueError:
        pass
    # Dotted netmask - must have contiguous 1s followed by 0s
    pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if re.match(pattern, subnet):
        try:
            parts = [int(p) for p in subnet.split(".")]
            if not all(0 <= p <= 255 for p in parts):
                return False
            # Convert to 32-bit integer
            num = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
            # Valid netmask: all 1s followed by all 0s in binary
            inv = num ^ 0xffffffff
            return (inv + 1) & inv == 0
        except (ValueError, IndexError):
            return False
    return False


def normalize_subnet(subnet: str) -> str:
    """Return subnet in a clean string form."""
    subnet = subnet.strip()
    try:
        val = int(subnet)
        if 0 <= val <= 32:
            return str(val)
    except ValueError:
        pass
    return subnet


def ip_to_int(ip: str) -> int:
    """Convert IPv4 string to integer for sorting/comparison."""
    parts = ip.strip().split(".")
    result = 0
    for p in parts:
        result = result * 256 + int(p)
    return result
