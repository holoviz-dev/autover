import os
import json
import importlib

from setuptools import setup, find_packages

def embed_version(basepath, reponame, ref='v0.2.1'):
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
    name='pkg_depend',
    version=get_setup_version("pkg_depend"),
    packages = find_packages(),
    package_data = {'pkg_depend': ['.version']},
    install_requires = ['autover'],
    entry_points = {
        'console_scripts': ['tmpverify=pkg_depend.tests:main'],
    },
    url = "http://",
    license = "BSD",
    description = "Example of depending on autover"    
)


if __name__=="__main__":
    setup(**setup_args)
