from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openfret",
    version="0.1.0",
    author="Jieming Li",
    author_email="jmli@umich.edu",
    description="A standardized format for single-molecule FRET data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openfret",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/openfret/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Bio-physics",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Science/Research",
    ],
    install_requires=[
    ],
)