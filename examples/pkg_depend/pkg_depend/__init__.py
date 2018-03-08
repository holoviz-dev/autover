try:
    from autover.version import Version
    versionobj = Version(release=None, fpath=__file__,
                         archive_commit="$Format:%h$", reponame="pkg_depend")
    __version__ = str(versionobj)
except:
    import os, json
    __version__ = json.load(open(os.path.join(os.path.split(__file__)[0],
                                              '.version'), 'r'))['version_string']
