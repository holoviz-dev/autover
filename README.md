[![Build Status](https://travis-ci.org/ioam/autover.svg?branch=master)](https://travis-ci.org/ioam/autover)
[![Appveyor build status](https://ci.appveyor.com/api/projects/status/eiy3sn7hja2nf6dc/branch/master?svg=true)](https://ci.appveyor.com/project/ioam/autover/branch/master)



Autover provides:

  1. Consistent and up-to-date `__version__` strings for Python
     packages; see the [Version
     class](https://github.com/ioam/autover/blob/master/autover/__init__.py).

  2. A script to import and print the library version and filesystem
     location for each Python package specified; see the [autover
     script](https://github.com/ioam/autover/blob/master/scripts/autover).

Authors: Jean-Luc Stevens, Chris Ball and James A. Bednar

# Versioning

(some intro)

## Usage

The expected way for your-package to use autover is by bundling
version.py.  An outline of how to do this is below, but you can also
follow the example [bundle
autover](https://github.com/ioam/autover/tree/master/examples/pkg_bundle)
package.

  1. copy autover.py into your project's git root directory and commit
     to git.
  
  2. `import autover` and call `autover.get_setup_version(...)` in
     your `setup.py` to get up to date version.
  
  3. make sure at package time that the `.version` json file is included
     in your package e.g. by adding `your-package/.version` to
     `MANIFEST.in` and `include_package_data=True` in
     `setup()`. (`version.py` will be included automatically unless you
     do something to stop that.)
     
  4. put the following `in your-package/__init__.py`:

```python
try:
    import autover
    __version__ = autover.Version(...)
except:
    import os, json
    __version__ = json.load(... '.version')
```

     The first path above (`import autover`) is for developers who are
     either in the git repository, or have done a `python setup.py
     develop` install, or have the git repository on their
     `PYTHONPATH`. I.e. if `import your-package` from the git repo is
     possible, so is `import autover`. The second path is for people
     who are installing a `your-package` package: no autover present
     or needed, because a `.version` file is present in the package.


There are alternative ways to use autover, including [via
param](https://github.com/ioam/autover/tree/master/examples/pkg_params)
or [depending on
autover](https://github.com/ioam/autover/tree/master/examples/pkg_depend).
