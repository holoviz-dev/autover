from autover.version import Version

versionobj = Version(release=None, fpath=__file__,
                     archive_commit="$Format:%h$", reponame="pkg_bundle")
__version__ = str(versionobj)
