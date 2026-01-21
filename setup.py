#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="norn-temmplates-engine",
    version="0.0.0",
    packages=find_packages(include=["norn_templates_engine", "norn_templates_engine.*", "cmd.*"]),
    entry_points={
        "console_scripts": [
        ]
    }
)