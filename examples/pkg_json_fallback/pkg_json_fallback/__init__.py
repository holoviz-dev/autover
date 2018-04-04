# Only testing the JSON fallback. See pkg_bundle or pkg_depend for complete example.
import os, json
__version__ = json.load(open(os.path.join(os.path.dirname(__file__),'.version'), 'r'))['version_string']

