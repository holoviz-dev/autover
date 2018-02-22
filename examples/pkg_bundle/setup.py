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
    name='pkg_bundle',
    version=get_setup_version("pkg_bundle"),
    packages = ["pkg_bundle"],
    scripts = ["scripts/tmpverify"],
)


if __name__=="__main__":
    setup(**setup_args)
