from setuptools import setup, find_packages

setup(
    name="deeptune",  # This should be the name of your package
    version="0.1.2",
    description="Python SDK for Deeptune Text-to-Speech API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Deeptune",
    author_email="blair@deeptune.com",
    url="https://github.com/yourusername/blair-wdq",  # Update this URL to your repository
    packages=find_packages(
        include=["deeptune"]
    ),  # Adjust this if your package structure is different
    install_requires=[
        "requests",  # Add other dependencies if necessary
        "pydantic",
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
