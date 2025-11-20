"""Setup configuration for ETH Gas Tracker."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="eth-gas-tracker",
    version="2.0.0",
    author="pavlenkotm",
    description="Advanced Python CLI for monitoring Ethereum and EVM-compatible blockchain gas prices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pavlenkotm/eth-gas-tracker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.9",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "excel": ["openpyxl>=3.1.0"],
        "notifications": ["plyer>=2.1.0"],
        "all": ["openpyxl>=3.1.0", "plyer>=2.1.0"],
    },
    entry_points={
        "console_scripts": [
            "ethgas=ethgas.main:main",
        ],
    },
)
