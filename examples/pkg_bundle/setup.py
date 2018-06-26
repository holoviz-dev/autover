from setuptools import setup, find_packages

from version import get_setup_version

setup_args = dict(
    name='pkg_bundle',
    version=get_setup_version(__file__,"pkg_bundle",archive_commit="$Format:%h$"),
    packages = find_packages(),
    include_package_data=True,    
    entry_points = {
        'console_scripts': ['tmpverify=pkg_bundle.tests:main'],
    },
    url = "http://",
    license = "BSD",
    description = "Example of bundling autover"
)


if __name__=="__main__":
    setup(**setup_args)
