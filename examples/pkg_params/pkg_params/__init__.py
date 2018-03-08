from param.version import Version

versionobj = Version(fpath=__file__,archive_commit="$Format:%h$", reponame="pkg_params")
__version__ = str(versionobj)
