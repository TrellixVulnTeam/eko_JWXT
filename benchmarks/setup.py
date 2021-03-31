# -*- coding: utf-8 -*-
# Installation script for python
from setuptools import setup, find_packages

setup(
    name="ekomark",
    author="A.Candido, F. Hekhorn, G.Magni",
    version="0.1.0",
    description="eko benchmark",
    # package_dir={"": "."},
    packages=find_packages("."),
    package_data={"ekomark": ["data/external/LHA.yaml",]},
    install_requires=[
        "eko",
        "pandas",
        "banana-hep",
        "sqlalchemy",
        "matplotlib",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": ["ekonavigator=ekomark.navigator:launch_navigator",],
    },
    python_requires=">=3.7",
)
