from setuptools import setup, find_packages

setup_args = dict(
    name='pkg_depend',
    version=autover.version.get_setup_version(__file__,"pkg_depend",archive_commit="$Format:%h$"),
    packages = find_packages(),
    include_package_data = True,
    entry_points = {
        'console_scripts': ['tmpverify=pkg_depend.tests:main'],
    },
    install_requires = ['autover'],
    url = "http://",
    license = "BSD",
    description = "Example of depending on autover"
)


if __name__=="__main__":
    setup(**setup_args)
