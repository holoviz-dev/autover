from .version import Version

try:
    versionobj = Version(fpath=__file__, archive_commit="$Format:%h$", reponame="autover")
    __version__ = str(versionobj)
except:
    import json
    __version__ = json.load(open('.version', 'r'))['version_string']

from .report import report  # noqa: api
