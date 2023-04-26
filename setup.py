import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("requirements.test.txt") as f:
    tests_requirements = f.read().splitlines()

from src.httpstreamxml import version

setuptools.setup(
    name='http-stream-xml',
    version=version.VERSION,
    author="Andrey Sorokin",
    author_email="andrey@sorokin.engineer",
    description="Parse XML in HTTP response on the fly, by chunks",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://http-stream-xml.readthedocs.io/en/latest/",
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    keywords='http stream xml chunked',
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],
 )