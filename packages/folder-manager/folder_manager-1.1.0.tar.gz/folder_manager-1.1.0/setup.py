# setup.py
from setuptools import setup, find_packages

setup(
    name="folder_manager",
    version="1.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add any dependencies here
    ],
    author="Javer Valino",
    description="A simple folder management library designed to manage folders and files. It provides functionalities to create, list, count, and delete files and folders, making it a versatile tool for file management. The package is designed to be OS-independent, ensuring compatibility with both Windows and Unix-based systems.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/phintegrator/folder_manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
