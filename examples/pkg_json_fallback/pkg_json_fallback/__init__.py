import json
import os

__version__ = json.load(open(os.path.join(os.path.split(__file__)[0],
                                          '.version'), 'r'))['version_string']

