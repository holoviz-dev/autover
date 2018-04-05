from setuptools import setup, find_packages

def embed_version(basepath, ref='v0.2.1'):
    """
    Autover is purely a build time dependency in all cases (conda and
    pip) except for when you use pip's remote git support [git+url] as
    1) you need a dynamically changing version and 2) the environment
    starts off clean with zero dependencies installed.

    This function acts as a fallback to make Version available until
    PEP518 is commonly supported by pip to express build dependencies.
    """
    import io, zipfile, os
    try:    from urllib.request import urlopen
    except: from urllib import urlopen
    response = urlopen('https://github.com/ioam/autover/archive/{ref}.zip'.format(ref=ref))
    zf = zipfile.ZipFile(io.BytesIO(response.read()))
    ref = ref[1:] if ref.startswith('v') else ref
    embed_version = zf.read('autover-{ref}/autover/version.py'.format(ref=ref))
    with open(os.path.join(basepath, 'version.py'), 'wb') as f:
        f.write(embed_version)


def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    import json, importlib, os
    basepath = os.path.dirname(os.path.abspath(__file__))
    version_file_path = os.path.join(basepath, reponame, '.version')
    version = None
    try: version = importlib.import_module("version") # bundled
    except:
        try: from autover import version # available as package
        except:
            try: from param import version # available via param
            except:
                embed_version(basepath) # download
                version = importlib.import_module("version")

    if version is not None:
        return version.Version.setup_version(basepath, reponame, archive_commit="$Format:%h$")
    else:
        print("WARNING: autover unavailable. If you are installing a package, this warning can safely be ignored. If you are creating a package or otherwise operating in a git repository, you should refer to autover's documentation to bundle autover or add it as a dependency.")
        return json.load(open(version_file_path, 'r'))['version_string']


setup_args = dict(
    name='pkg_params',
    version=get_setup_version("pkg_params"),
    packages = find_packages(),
    include_package_data = True,
    entry_points = {
        'console_scripts': ['tmpverify=pkg_params.tests:main'],
    },
    # TODO: need to investigate pip's handling of the postN+gSHA scheme...
    # note: .post required (>1.5.1 won't match 1.5.1.postN+gSHA releases)
    install_requires = ['param >=1.6.0'],
    url = "http://",
    license = "BSD",
    description = "Example of depending on autover via param"
)


if __name__=="__main__":
    setup(**setup_args)
