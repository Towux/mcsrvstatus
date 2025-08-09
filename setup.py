"""Setup configuration for mcsrvstatus library."""

from setuptools import setup, find_packages
import os

# Read description from README if it exists
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="mcsrvstatus",
    version="1.0.5",
    author="Towux",
    author_email="",
    description="Python library for mcsrvstat.us API - Minecraft server status checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Towux/mcsrvstatus",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords="minecraft server status api mcsrvstat bedrock java async",
    project_urls={
        "Bug Reports": "https://github.com/Towux/mcsrvstatus/issues",
        "Source": "https://github.com/Towux/mcsrvstatus",
        "Documentation": "https://github.com/Towux/mcsrvstatus#readme",
    },
)
