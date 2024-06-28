import json
from setuptools import setup, find_packages # type:ignore

with open("version.json", "r", encoding="utf-8") as f: version: str = json.load(f)["version"]

setup(
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
