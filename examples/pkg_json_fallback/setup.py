from setuptools import setup, find_packages


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
