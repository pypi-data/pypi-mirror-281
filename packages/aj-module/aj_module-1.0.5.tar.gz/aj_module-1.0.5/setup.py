from setuptools import setup, find_packages # type:ignore

setup(
    name='aj-module',
    version='1.0.5',
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
