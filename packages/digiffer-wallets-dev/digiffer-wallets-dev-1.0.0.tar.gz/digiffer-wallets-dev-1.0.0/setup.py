# setup.py

from setuptools import setup, find_packages

setup(
    name="digiffer-wallets-dev",
    version="1.0.0",
    description="A Python package to interact with Digiffer Wallets API.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    tests_require=[
        "unittest",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
