try:
    # a developer install; version.py will be available on path
    from version import Version
    __version__ = str(Version(fpath=__file__,archive_commit="$Format:%h$",reponame="pkg_bundle"))
except:
    # an installed package; pkg_bundle/.version will be present
    import json
    __version__ = json.load(open(os.path.join(os.path.dirname(__file__),'.version'),'r'))['version_string']
