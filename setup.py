import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rssi",
    version="1.0.0",
    author="Juan Antonio Villlagomez",
    author_email="email@juan-antonio.me",
    description="Easy to use package for RSSI scanning and utilizing RSSI-based self-localization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://jvillagomez@bitbucket.org/jvillagomez/rssi-module.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
