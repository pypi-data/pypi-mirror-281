"""
treegp.
"""

# The version is stored in _version.py as recommended here:
# http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
from ._version import __version__, __version_info__

from .gp_interpolation import *

__all__ = [
    "interpolateOverDefectsGP",
]
