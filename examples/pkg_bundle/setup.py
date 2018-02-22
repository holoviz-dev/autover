import os
import json

from setuptools import setup


def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    basepath = os.path.split(__file__)[0]
    version_file_path = os.path.join(basepath, reponame, '.version')
    return importlib.import_module(reponame + ".version") # Bundled


setup_args = dict(
    name='pkg_bundle',
    version=get_setup_version("pkg_bundle"),
    packages = ["pkg_bundle"],
    scripts = ["scripts/tmpverify"],
)


if __name__=="__main__":
    setup(**setup_args)
