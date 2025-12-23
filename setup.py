from setuptools import setup, find_packages
import os



setup(
    name="cppforge",
    version="0.2.0",
    description="A CLI for managing C++ projects",
    author="Rose Tovar",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "cppforge=cppforge.main:main",
        ],
    },
    install_requires=["jinja2", "pyyaml"],
)
