from setuptools import setup, find_packages

setup(
    name="blair-wdq",  # This can remain with hyphens for PyPI
    version="0.1.1",
    description="Python SDK for Deeptune Text-to-Speech API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/blair-wdq",  # Update this URL to your repository
    packages=find_packages(
        include=["blair_wdq", "blair_wdq.*"]
    ),  # Ensure it matches your directory
    install_requires=[
        "requests",  # Add other dependencies if necessary
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)
