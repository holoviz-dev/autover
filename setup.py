import os
import sys
import json

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    basepath = os.path.split(__file__)[0]
    version_file_path = os.path.join(basepath, reponame, '.version')
    try:
        from autover import Version
        vstring =  Version.get_setup_version(basepath, reponame, dirty='strip',
                                             archive_commit="$Format:%h$")

        try: # Will only work if in a git repo and git is available
            describe_string = Version.get_setup_version(basepath, reponame,
                                                        describe=True,
                                                        dirty='strip',
                                                        archive_commit="$Format:%h$")
            with open(version_file_path, 'w') as f:
                f.write(json.dumps({'git_describe':describe_string,
                                    'version_string': vstring}))
        except:
            pass
        return vstring

    except ImportError:
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
