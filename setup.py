import codecs
import os
import os.path

import setuptools

with open("README.rst") as fh:
    long_description = fh.read()

with open("requirements.in") as f:
    requirements = f.read().splitlines()


# Solution from https://packaging.python.org/guides/single-sourcing-package-version/
def read(rel_path: str) -> str:
    """Read file."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    """Parse version from file content."""
    for line in read(rel_path).splitlines():
        if line.startswith("VERSION"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="http-stream-xml",
    version=get_version("src/http_stream_xml/version.py"),
    author="Andrey Sorokin",
    author_email="andrey@sorokin.engineer",
    description=(
        "Parse XML in HTTP response on the fly, by chunks - for example NCBI (PubMed) Entrez."
    ),
    entry_points={
        "console_scripts": [
            "garmin-daily=garmin_daily.google_sheet:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/andgineer/http-stream-xml",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=requirements,
    python_requires=">=3.11",
    keywords="http stream xml chunked",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
