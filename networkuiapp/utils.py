"""Helper utilities and decorators."""
import re
import ipaddress
from flask import flash
from markupsafe import Markup


def make_dropdown(model, field: str) -> list[tuple[int, str]]:
    """Returns the elements for a drop down"""
    # ? is this less pythonic?
    return [(g.id, getattr(g, field)) for g in model.query.all()]


def validate_ip_address_string(ip_address: str) -> bool:
    """Check whether the given string is an IP address or not

    Args:
        ip_address (str): a string accepted from the user

    Returns:
        bool: True if the given string is a valid IP address
    """
    # https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(regex, ip_address):
        return True
    return False


def ip_mask_calculations(ip: str) -> dict:
    """Calculate the broadcast and network addresses and limit from a CIDR

    Args:
        ip (string): an IP address in the form of CIDR notation

    Returns:
        dict: a dict with broadcast_addr, network_addr and network_addr
    """
    net = ipaddress.IPv4Network(ip, False)

    if ip:
        try:
            if int(ip.rsplit("/")[1]) < 31:
                broadcast_addr = net.broadcast_address
                network_addr = net.network_address
                limit = f"{ net.network_address + 1} - {net.broadcast_address - 1}"
                return {
                    "broadcast_addr": broadcast_addr,
                    "network_addr": network_addr,
                    "limit": limit,
                }
        except:
            # yeah this is not the right way to handle errors
            pass
        return {"broadcast_addr": None, "network_addr": None, "limit": ip}


def check_ip_belongs_subnet(ip: str, nw: str) -> bool:
    """Check whether an IP belongs to a subnet or not

    Args:
        ip (str): IP address to be checked
        nw (str): Network

    Returns:
        bool: True if the IP address belongs to the subnet
    """
    if ip and nw:
        return ipaddress.ip_address(ip) in ipaddress.ip_network(nw, strict=False)
    return False


def make_cidr_range(template_and_subnets) -> dict:
    """Creates a dict where Key: is Template Name and Value is CIDR limit text

    Args:
        template_and_subnets: Query return with template name and subnet limit

    Returns:
        dict: key: Template name, Value: CIDR limit
    """
    return {
        handicap_name: ip_mask_calculations(cidr_notation)["limit"]
        for handicap_name, cidr_notation in template_and_subnets
        if cidr_notation
    }


# fmt: off
def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(Markup(f"Error in <em><u>{getattr(form, field).label.text}</u></em>: {error}"), category)
