import os
import json
import importlib

from setuptools import setup


def embed_version(basepath, reponame, ref='pep440-after-pep440_fix'):
    """
    Autover is purely a build time dependency in all cases (conda and
    pip) except for when you use pip's remote git support [git+url] as
    1) you need a dynamically changing version and 2) the environment
    starts off clean with zero dependencies installed.

    This function acts as a fallback to make Version available until
    PEP518 is commonly supported by pip to express build dependencies.
    """
    import io, zipfile
    try:    from urllib.request import urlopen
    except: from urllib import urlopen
    response = urlopen('https://github.com/ioam/autover/archive/{ref}.zip'.format(ref=ref))
    zf = zipfile.ZipFile(io.BytesIO(response.read()))
    embed_version = zf.read('autover-{ref}/autover/version.py'.format(ref=ref))
    with open(os.path.join(basepath, reponame, 'version.py'), 'wb') as f:
        f.write(embed_version)


def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    basepath = os.path.split(__file__)[0]
    version_file_path = os.path.join(basepath, reponame, '.version')
    version = None
    try: version = importlib.import_module(reponame + ".version") # Bundled
    except:  # autover available as package
        try: from autover import version
        except:
            try: from param import version # Try to get it from param
            except:
                embed_version(basepath, reponame)
                version = importlib.import_module(reponame + ".version")

    if version is not None:
        return version.Version.setup_version(basepath, reponame, dirty='strip',
                                             archive_commit="$Format:%h$")
    else:
        print("WARNING: To get fully up-to-date version information 'pip install autover'.")
        return json.load(open(version_file_path, 'r'))['version_string']

setup_args = dict(
    name='autover',
    version=get_setup_version("autover"),
    description='Autover provides consistent and up-to-date `__version__` strings for Python packages.',
    long_description=open('README.rst').read() if os.path.isfile('README.rst') else 'Consult README.rst',
    author= "IOAM",
    author_email= "developers@topographica.org",
    maintainer="IOAM",
    maintainer_email="developers@topographica.org",
    platforms=['Windows', 'Mac OS X', 'Linux'],
    license='BSD',
    url='http://github.com/ioam/autover/',
    packages = ["autover"],
    provides = ["autover"],
    include_package_data=True,
    scripts = ["scripts/autover","scripts/tmpverify"],
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
