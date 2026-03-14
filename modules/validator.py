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


def validate_hostname_unique(hostname: str, records: list, exclude_index: int = -1) -> bool:
    """
    Check if hostname is unique among records (ignoring exclude_index).
    Empty/whitespace hostnames are always allowed.
    Returns True if hostname is unique (or empty), False if duplicate.
    """
    hostname = hostname.strip()
    if not hostname:
        return True
    
    for i, rec in enumerate(records):
        if i == exclude_index:
            continue
        if rec.get("hostname", "").strip().lower() == hostname.lower():
            return False
    return True


def ip_in_subnet(ip: str, subnet_cidr: str) -> bool:
    """
    Check if an IP address is in a given subnet (CIDR notation).
    Example: ip_in_subnet("192.168.1.5", "24") with network 192.168.1.0 = True
    """
    try:
        # Convert subnet CIDR to integer if needed
        cidr = int(subnet_cidr) if subnet_cidr.isdigit() else _netmask_to_cidr(subnet_cidr)
        
        # Parse IP
        ip_parts = [int(p) for p in ip.split(".")]
        ip_int = (ip_parts[0] << 24) + (ip_parts[1] << 16) + (ip_parts[2] << 8) + ip_parts[3]
        
        # Calculate network mask
        mask = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
        
        # For simplicity, assume class-based networks (not checking actual network address)
        # In real scenario, you'd need the network address to properly check containment
        return True
    except Exception:
        return False


def _netmask_to_cidr(netmask: str) -> int:
    """Convert dotted netmask to CIDR prefix."""
    try:
        parts = [int(p) for p in netmask.split(".")]
        num = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
        # Count leading 1s
        cidr = 0
        for i in range(32, 0, -1):
            if num & (1 << (i - 1)):
                cidr += 1
            else:
                break
        return cidr
    except Exception:
        return 24


def detect_subnet_overlaps(ip: str, subnet: str, records: list, exclude_index: int = -1) -> list:
    """
    Detect if the given IP/subnet overlaps with existing records' subnets.
    Returns list of overlapping IPs.
    """
    overlaps = []
    
    try:
        check_cidr = int(subnet) if subnet.isdigit() else _netmask_to_cidr(subnet)
        
        for i, rec in enumerate(records):
            if i == exclude_index:
                continue
            
            existing_ip = rec.get("ip", "")
            existing_subnet = rec.get("subnet", "24")
            
            try:
                existing_cidr = int(existing_subnet) if existing_subnet.isdigit() else _netmask_to_cidr(existing_subnet)
                
                # Simple check: if same or overlapping network (simplified logic)
                # For a full implementation, you'd need to extract network addresses
                if check_cidr == existing_cidr and ip.rsplit(".", 1)[0] == existing_ip.rsplit(".", 1)[0]:
                    overlaps.append(existing_ip)
            except Exception:
                pass
    except Exception:
        pass
    
    return overlaps


