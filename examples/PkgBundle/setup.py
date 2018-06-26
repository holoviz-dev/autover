from setuptools import setup, find_packages

from version import get_setup_version

package_name = "pkg_bundle"

setup_args = dict(
    name=package_name,
    version=get_setup_version(__file__,"PkgBundle",package_name),
    packages = find_packages(),
    include_package_data=True,    
    entry_points = {
        'console_scripts': ['tmpverify=%s.tests:main'%package_name],
    },
    url = "http://",
    license = "BSD",
    description = "Example of bundling autover"
)


if __name__=="__main__":
    setup(**setup_args)
