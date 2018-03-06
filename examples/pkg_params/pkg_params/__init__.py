try:    from param.version import Version
except: from .version import Version

try:
    versionobj = Version(release=None, fpath=__file__,
                         archive_commit="$Format:%h$", reponame="pkg_params")
    __version__ = str(versionobj)
except:
    import os, json
    __version__ = json.load(open(os.path.join(os.path.split(__file__)[0],
                                              '.version'), 'r'))['version_string']
