import json
from setuptools import setup, find_packages # type:ignore

with open("data.json", "r", encoding="utf-8") as f: version: str = json.load(f)["version"]

desc: str = """
# AJ-Pack
This is my little module for python.
Just enjoy it and don't do something illegal ;) have fun <3
"""

setup(
    author="AJ-Holzer",
    description=desc,
    url="https://github.com/AJ-Holzer/AJ-Module",
    license="MIT",
    name='ajpack',
    version=version,
    packages=find_packages(),
    install_requires=[
        "pyzipper",
        "opencv-python",
        "requests",
        "Pillow",
        "keyboard",
        "pywin32",
        "psutil",
        "winshell",
        "plyer",
        "customtkinter"
    ],
    entry_points={
        'console_scripts': [
            # command lines
        ],
    },
)
