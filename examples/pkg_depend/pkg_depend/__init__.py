try:
    from autover.version import Version
    __version__ = str(Version(fpath=__file__,archive_commit="$Format:%h$",reponame="pkg_depend"))
except:
    import os, json
    __version__ = json.load(open(os.path.join(os.path.dirname(__file__),'.version'),'r'))['version_string']
