# setup.py

from setuptools import setup, find_packages

setup(
    name="simplepackageEx",
    version="0.0.1",
    packages=find_packages(),
    author="MyName",
    author_email="myemail@example.com",
    description="A simple arithmetic package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/myusername/simplepackage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
