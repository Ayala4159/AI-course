"""Setup script for task_manager package."""

from setuptools import setup, find_packages

setup(
    name="task_manager",
    version="1.0.0",
    description="A comprehensive Python task management system",
    author="Development Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-cov>=3.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
