# setup.py
from setuptools import setup, find_packages

setup(
    name="pyfally",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Fally",
    author_email="hemmem17@gmail.com",
    description="A Python library to shorten your urls",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HEMMEM97/pyfally.git",  # Replace with your GitHub repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
