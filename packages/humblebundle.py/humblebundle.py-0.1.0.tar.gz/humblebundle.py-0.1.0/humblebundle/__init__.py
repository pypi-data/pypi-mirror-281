"""
HumbleBundle Unofficial Client

This package provides a client interface to interact with the HumbleBundle website.
It includes functionalities to retrieve bundle information and choice options for specific months and years.

Modules:
    get: Contains low-level functions for making web requests.

Usage:
    import humblebundle
    bundles = humblebundle.bundles(['bundle_name'])
    choices = humblebundle.choices('january', 2023)
"""
from . import get