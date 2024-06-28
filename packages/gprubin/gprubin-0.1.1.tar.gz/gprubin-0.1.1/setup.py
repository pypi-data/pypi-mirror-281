#!/usr/bin/env python

"""Setup script."""

from __future__ import print_function
import glob
import sys
import os
import re
import setuptools
from setuptools import setup, find_packages

# Print some useful information in case there are problems, this info will help troubleshoot.
print("Using setuptools version", setuptools.__version__)
print("Python version = ", sys.version)

with open("README.rst") as f:
    long_description = f.read()

# Read in the version from gprubin/_version.py
# cf. http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
version_file = os.path.join("gprubin", "_version.py")
with open(version_file, "rt") as f:
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    txt = f.read()
    mo = re.search(VSRE, txt, re.M)
    if mo:
        gprubin_version = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (version_file,))
print("gprubin version is %s" % (gprubin_version))

# Package name
name = "gprubin"

# Packages
packages = find_packages()

# Scripts (none yet, but if we make any, they will live in scripts/)
scripts = []

# Dependencies
dependencies = [
    "numpy",
    "scipy",
    "treegp>=1.2.0",
    "jax",
]

package_data = {}

setup(
    name=name,
    description="gprubin",
    long_description=long_description,
    license="BSD License",
    classifiers=[
        "Topic :: Scientific/Engineering :: Astronomy",
        "Intended Audience :: Science/Research",
    ],
    author="PFLeget",
    url="https://github.com/PFLeget/gprubin",
    download_url="https://github.com/PFLeget/gprubin/releases/tag/v%s.zip"
    % gprubin_version,
    install_requires=dependencies,
    version=gprubin_version,
    packages=packages,
    scripts=scripts,
)
