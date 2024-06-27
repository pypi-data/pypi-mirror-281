import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proharmed",
    version="0.0.5",
    author="Klaudia Adamowicz",
    author_email='klaudia.adamowicz@uni-hamburg.de',
    url='http://pypi.python.org/pypi/proharmed/',
    license='LICENSE',
    description="Collection of scripts for ProHarMeD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Science/Research',
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',
    install_requires=[
        "numpy>=1.20.0,<=1.26.4",
        "pandas>=1.2.0,<=2.2.2",
        "requests>=2.26.0",
        "gprofiler-official>=1.0.0",
        "httplib2>=0.21.0",
        "ratelimit>=2.2.1",
        "mygene",
        "seaborn",
        "psutil",
        "upsetplot"
    ]
)
