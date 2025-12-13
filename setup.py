from setuptools import setup, find_packages

setup(
    name="cppforge",
    version="0.1.0",
    description="A CLI for managing C++ projects",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cppforge": ["../templates/*.template"],    
    },
    entry_points={
        "console_scripts": [
            "cppforge=cppforge.main:main",
        ],
    },
    install_requires=["jinja2"],
)
