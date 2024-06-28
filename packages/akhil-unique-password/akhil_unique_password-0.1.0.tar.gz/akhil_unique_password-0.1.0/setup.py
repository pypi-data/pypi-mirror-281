# setup.py

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="akhil-unique-password",
    version="0.1.0",
    author="Akhil Siddabattula",
    author_email="akhilsiddabattula@gmail.com",
    description="A simple Python library for generating random passwords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/random-password-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
