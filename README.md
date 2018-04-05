[![Build Status](https://travis-ci.org/ioam/autover.svg?branch=master)](https://travis-ci.org/ioam/autover)
[![Appveyor build status](https://ci.appveyor.com/api/projects/status/eiy3sn7hja2nf6dc/branch/master?svg=true)](https://ci.appveyor.com/project/ioam/autover/branch/master)


Autover provides:

  1. Consistent and up-to-date `__version__` strings for Python
     packages; see the [Version
     class](https://github.com/ioam/autover/blob/master/autover/version.py).

  2. Reporting of version and filesystem location for requested Python
     packages and shell commands.

# Versioning

(docs coming soon...)


# Reporting

`autover report` can be used to report the versions of specified
packages. And because the same version of a package may be available
from many possible different sources (e.g. various conda channels,
pypi servers, system package managers, built from source, etc), and
because a package could be installed multiple times on a particular
system, autover report also includes the filesystem location.

At the commandline, `autover report pkg1 pkg2 cmd1 cmd2 ...` will
report the version and filesystem location for the specified python
packages and shell commands.

Reporting may also be done from within python itself, e.g. `import
autover ; autover.report("numpy","pandas","python","conda")`.

(TODO: e.g. conda is name of command and python package...)