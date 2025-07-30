from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kapfinance",
    version="0.1.3",
    author="Mert Kurtçu",
    author_email="mertkurtcu.official@gmail.com",
    description="A Python class for managing financial statement data from HTML-based XLS files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mertkurtcu/kapfinance",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'matplotlib>=3.0.0', 
        'lxml', 
        'openpyxl', 
    ],
)
