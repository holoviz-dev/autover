try:    from autover.version import Version
except: from .version import Version

try:
    versionobj = Version(release=None, fpath=__file__,
                         archive_commit="$Format:%h$", reponame="pkg_depend")
    __version__ = str(versionobj)
except:
    import json
    __version__ = json.load(open('.version', 'r'))['version_string']

