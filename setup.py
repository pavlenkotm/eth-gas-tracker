"""Setup configuration for eth-gas-tracker."""
from pathlib import Path
from setuptools import setup, find_packages

# Read version from __init__.py
init_file = Path(__file__).parent / "ethgas" / "__init__.py"
version = "0.1.0"
for line in init_file.read_text().splitlines():
    if line.startswith("__version__"):
        version = line.split("=")[1].strip().strip('"').strip("'")
        break

# Read README for long description
readme = Path(__file__).parent / "README.md"
long_description = readme.read_text(encoding="utf-8") if readme.exists() else ""

setup(
    name="eth-gas-tracker",
    version=version,
    author="pavlenkotm",
    description="Tiny Python CLI that reads Ethereum gas using eth_feeHistory (no API keys)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pavlenkotm/eth-gas-tracker",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.9",
    ],
    entry_points={
        "console_scripts": [
            "ethgas=ethgas.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
    keywords="ethereum gas tracker blockchain web3",
)
