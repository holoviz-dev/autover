from setuptools import setup, find_packages

def embed_version(basepath, ref='v0.2.5'):
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
    # NOTE: This is not the complete function - only testing the final JSON fallback
    # See pkg_bundle or pkg_depend for complete example.
    import os, json
    basepath = os.path.dirname(__file__)
    version_file_path = os.path.join(basepath, reponame, '.version')
    return json.load(open(version_file_path, 'r'))['version_string']

setup_args = dict(
    name='pkg_json_fallback',
    version=get_setup_version("pkg_json_fallback"),
    packages = find_packages(),
    include_package_data = True,
    entry_points = {
        'console_scripts': ['tmpverify=pkg_json_fallback.tests:main'],
    },
    url = "http://",
    license = "BSD",
    description = "Example of falling back to JSON if all else fails"
)


if __name__=="__main__":
    setup(**setup_args)
