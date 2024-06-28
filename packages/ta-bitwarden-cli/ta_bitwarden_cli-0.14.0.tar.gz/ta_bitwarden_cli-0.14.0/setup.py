#!/usr/bin/env python

"""The setup script."""
import sys

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

sys.path.append("ta_bitwarden_cli")
sys.path.append("download_bitwarden")
from download_bitwarden import DownloadBitwarden  # noqa


class Download(build_py, DownloadBitwarden):
    """Static class that just downloads Bitwarden cli binary."""

    def run(self):
        """Download Bitwarden CLI binary."""
        self.download_bitwarden()
        build_py.run(self)


with open("README.rst") as readme_file:
    readme = readme_file.read()

install_requirements = open("requirements.txt").readlines()

setup(
    author="Bohdan Sukhov",
    author_email="bohdan.sukhov@thoughtfulautomation.com",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Thoughtful BitWarden CLI Package",
    entry_points={
        "console_scripts": [
            "ta_bitwarden_cli=ta_bitwarden_cli.cli:main",
        ],
    },
    install_requires=install_requirements,
    long_description=readme,
    keywords="ta_bitwarden_cli",
    name="ta_bitwarden_cli",
    packages=find_packages(include=["ta_bitwarden_cli"]),
    include_package_data=True,
    test_suite="tests",
    url="https://www.thoughtful.ai/",
    version="0.14.0",
    zip_safe=False,
    cmdclass={"build_py": Download},
)
