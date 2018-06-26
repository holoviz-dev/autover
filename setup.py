import os

from setuptools import setup, find_packages

# Versioning autover depends on autover.
from autover.version import get_setup_version

setup_args = dict(
    name='autover',
    version=get_setup_version(__file__, "autover", archive_commit="$Format:%h$"),
    description='Autover provides consistent and up-to-date `__version__` strings for Python packages.',
    long_description=open('README.rst').read() if os.path.isfile('README.rst') else 'Consult README.rst',
    author= "IOAM",
    author_email= "developers@topographica.org",
    maintainer="IOAM",
    maintainer_email="developers@topographica.org",
    platforms=['Windows', 'Mac OS X', 'Linux'],
    license='BSD',
    url='http://github.com/ioam/autover/',
    packages = find_packages(),
    provides = ["autover"],
    package_data = {'autover':['.version']},
    include_package_data=True,
    scripts = ["scripts/autover"],
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries"]
)



if __name__=="__main__":
    setup(**setup_args)
