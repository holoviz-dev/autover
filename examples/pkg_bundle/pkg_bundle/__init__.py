try:    from autover.version import Version
except: from .version import Version
# TODO: Load from .version!

versionobj = Version(release=None, fpath=__file__,
                     archive_commit="$Format:%h$", reponame="pkg_bundle")
__version__ = str(versionobj)
