"""Setup script for AI History Analyser"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="ai-history-analyser",
    version="0.1.0",
    description="Analyze chat histories from AI assistants to identify unfinished projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/ai-history-analyser",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.1.0",
        "python-dateutil>=2.8.2",
        "tqdm>=4.66.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ai-history-analyser=ai_history_analyser.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

