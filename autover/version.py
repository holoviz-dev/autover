"""Provide consistent and up-to-date ``__version__`` strings for Python
packages.

It is easy to forget to update ``__version__`` strings when releasing
a project, and it is important that the ``__version__`` strings are
useful over the course of development even between releases,
especially if releases are infrequent.

This file provides a Version class that addresses both problems.
Version is meant to be a simple, bare-bones approach that focuses on (a)
ensuring that all declared version information matches for a release if
supplied, and (b) providing fine-grained version information via a
version control system (VCS) in between releases (c) allowing versions
to be specified with tags alone.  Other approaches like versioneer.py
can automate more of the process of making releases, but they require
more complex self-modifying code and code generation techniques than the
simple Python class declaration used here.

Currently, the only VCS supported is git, but others could be added
easily.

To use Version in a project that provides a Python package named
``package`` maintained in a git repository named ``packagegit``:

1. Make the Version class available for import from your package,
   either by adding the PyPI package "autover" as a dependency for your
   package, or by simply copying this file into ``package/autover.py``.

2. Assuming that the current version of your package is 1.0.0 (and you
   want to enforce this), add the following lines to your
   ``package/__init__.py``::

     from autover import Version
     __version__ = Version(release=(1,0,0), fpath=__file__,
                           commit="$Format:%h$", reponame="packagegit")

   (or ``from .version import Version`` if you copied the file directly.)

   You can supply release=None if you want to set the version purely via a tag.

3. Declare the version as a string in your package's setup.py file, e.g.::

     setup_args["version"]="1.0.0"

  This acts as an explicit check you can verify against. You can also set this
  up against the tag using:

      setup_args["version"]=get_setup_version("autover") # Your package name here

  To use this, adapt the get_setup_version function in autover/setup.py for use
  in your package's setup.py.


4. (Optional) In your package's setup.py script code for making a
   release, you can add a call to the Version.verify method. E.g.::

     setup_args = dict(name='package', version="1.0.0", ...)

     if __name__=="__main__":
          if 'upload' in sys.argv:
              import package
              package.__version__.verify(setup_args['version'])
          setup(**setup_args)

  This can help make sure the repository is in a good state before
  building a package (e.g not dirty).

4. Tag the version of the repository to be released with a string of
   the form v*.*.*, i.e. ``v1.0.0`` in this example.  E.g. for git::

     git tag -a v1.0.0 -m 'Release version 1.0.0' ; git push

  You need to use an annotated tag (i.e the -a flag) and you can use
  PEP440 compliant strings as long as they start with a 'v' e.g
  v1.0.1a1 v2.3rc5 etc.

If you chose to specify explicit version strings in setup.py and
__init__.py and used the verify method, running ``setup.py`` to make a
release via something like ``python setup.py register sdist upload``,
Python will verify that the version last tagged in the VCS is the same
as what is declared in the package and the setup.py, aborting the
release until either the tag is corrected or the declared version is
made to match the tag.

Releases installed without VCS information will then report the declared
release version if specified, otherwise it will read the .version file
containing the VSC information when the package was build . If live VCS
information is available and matches the specified repository name, then
the version reported from e.g. ``str(package.__version__)`` will provide
more detailed information about the precise VCS revision changes since
the release.  See the docstring for the Version class for more detailed
information.

If you used release=None in __init__.py and the get_setup_version
function in setup.py, all you need to get a live version string is set
an appropriate VCS tag. Note that to ensure this is always correct,
autover is required as a build dependency, otherwise the information
available in the .version file is used.

This file is in the public domain, provided as-is, with no warranty of
any kind expressed or implied.  Anyone is free to copy, modify,
publish, use, compile, sell, or distribute it under any license, for
any purpose, commercial or non-commercial, and by any means.  The
original file is maintained at:
https://github.com/ioam/autover/blob/main/autover/__init__.py

"""


__author__ = 'Jean-Luc Stevens'

import os, subprocess, json

def run_cmd(args, cwd=None):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=cwd)
    output, error = (str(s.decode()).strip() for s in proc.communicate())

    # Detects errors as _either_ a non-zero return code _or_ messages
    # printed to stderr, because the return code is erroneously fixed at 
    # zero in some cases (see https://github.com/holoviz/param/pull/389).
    if proc.returncode != 0 or len(error) > 0:
        raise Exception(proc.returncode, error)
    return output



class Version(object):
    """
    A simple approach to Python package versioning that supports PyPI
    releases and additional information when working with version
    control. When obtaining a package from PyPI, the version returned
    is a string-formatted rendering of the supplied release tuple.
    For instance, release (1,0) tagged as ``v1.0`` in the version
    control system will return ``1.0`` for ``str(__version__)``.  Any
    number of items can be supplied in the release tuple, with either
    two or three numeric versioning levels typical.

    During development, a command like ``git describe`` will be used to
    compute the number of commits since the last version tag, the short
    commit hash, and whether the commit is dirty (has changes not yet
    committed). Version tags must start with a lowercase 'v' and have a
    period in them, e.g. v2.0, v0.9.8 or v0.1 and may include the PEP440
    prerelease identifiers of 'a' (alpha) 'b' (beta) or 'rc' (release
    candidate) allowing tags such as v2.0.a3, v0.9.8.b3 or v0.1.rc5.

    Also note that when version control system (VCS) information is
    used, the number of commits since the last version tag is
    determined. This approach is often useful in practice to decide
    which version is newer for a single developer, but will not
    necessarily be reliable when comparing against a different fork or
    branch in a distributed VCS.

    For git, if you want version control information available even in
    an exported archive (e.g. a .zip file from GitHub), you can set
    the following line in the .gitattributes file of your project::

      __init__.py export-subst

    Note that to support pip installation directly from GitHub via git
    archive, a .version file must be tracked by the repo to supply the
    release number (otherwise only the short SHA is available).

    The PEP440 format returned is [N!]N(.N)*[{a|b|rc}N][.postN+SHA]
    where everything before .postN is obtained from the tag, the N in
    .postN is the number of commits since the last tag and the SHA is
    obtained via git describe. This later portion is only shown if the
    commit count since the last tag is non zero. Instead of '.post', an
    alternate valid prefix such as '.rev', '_rev', '_r' or '.r' may be
    supplied."""

    def __init__(self, release=None, fpath=None, commit=None, reponame=None,
                 commit_count_prefix='.post', archive_commit=None, **kwargs):
        """
        :release:      Release tuple (corresponding to the current VCS tag)
        :commit        Short SHA. Set to '$Format:%h$' for git archive support.
        :fpath:        Set to ``__file__`` to access version control information
        :reponame:     Used to verify VCS repository name.
        """
        self.fpath = fpath
        self._expected_commit = commit

        if release is not None or 'commit_count' in kwargs:
            print('WARNING: param.Version now supports PEP440 and a new tag based workflow. See param/version.py for more details')

        self.expected_release = release

        self._commit = None if (commit is None or commit.startswith("$Format")) else commit
        self._commit_count = None
        self._release = None
        self._dirty = False
        self._prerelease = None

        self.archive_commit= archive_commit

        self.reponame = reponame
        self.commit_count_prefix = commit_count_prefix

    @property
    def prerelease(self):
        """
        Either None or one of 'aN' (alpha), 'bN' (beta) or 'rcN'
        (release candidate) where N is an integer.
        """
        return self.fetch()._prerelease

    @property
    def release(self):
        "Return the release tuple"
        return self.fetch()._release

    @property
    def commit(self):
        "A specification for this particular VCS version, e.g. a short git SHA"
        return self.fetch()._commit

    @property
    def commit_count(self):
        "Return the number of commits since the last release"
        return self.fetch()._commit_count

    @property
    def dirty(self):
        "True if there are uncommited changes, False otherwise"
        return self.fetch()._dirty


    def fetch(self):
        """
        Returns a tuple of the major version together with the
        appropriate SHA and dirty bit (for development version only).
        """
        if self._release is not None:
            return self

        self._release = self.expected_release
        if not self.fpath:
            self._commit = self._expected_commit
            return self

         # Only git right now but easily extended to SVN, Mercurial, etc.
        for cmd in ['git', 'git.cmd', 'git.exe']:
            try:
                self.git_fetch(cmd)
                break
            except EnvironmentError:
                pass
        return self


    def git_fetch(self, cmd='git', as_string=False):
        commit_argument = self._commit
        output = None
        try:
            if self.reponame is not None:
                # Verify this is the correct repository (since fpath could
                # be an unrelated git repository, and autover could just have
                # been copied/installed into it).
                remotes = run_cmd([cmd, 'remote', '-v'],
                                  cwd=os.path.dirname(self.fpath))
                repo_matches = ['/' + self.reponame + '.git' ,
                                # A remote 'server:reponame.git' can also be referred
                                # to (i.e. cloned) as `server:reponame`.
                                '/' + self.reponame + ' ']
                if not any(m in remotes for m in repo_matches):
                    try:
                        output = self._output_from_file()
                        if output is not None:
                            self._update_from_vcs(output)
                    except: pass
            if output is None:
                output = run_cmd([cmd, 'describe', '--long', '--match',
                                  "v[0-9]*.[0-9]*.[0-9]*", '--dirty'],
                                 cwd=os.path.dirname(self.fpath))
            if as_string: return output
        except Exception as e1:
            try:
                output = self._output_from_file()
                if output is not None:
                    self._update_from_vcs(output)
                if self._known_stale():
                    self._commit_count = None
                if as_string: return output

                # If an explicit commit was supplied (e.g from git
                # archive), it should take precedence over the file.
                if commit_argument:
                    self._commit = commit_argument
                return

            except IOError:
                if e1.args[1] == 'fatal: No names found, cannot describe anything.':
                    raise Exception("Cannot find any git version tags of format v*.*")
                # If there is any other error, return (release value still useful)
                return self

        self._update_from_vcs(output)


    def _known_stale(self):
        """
        The commit is known to be from a file (and therefore stale) if a
        SHA is supplied by git archive and doesn't match the parsed commit.
        """
        if self._output_from_file() is None:
            commit = None
        else:
            commit = self.commit

        known_stale = (self.archive_commit is not None
                       and not self.archive_commit.startswith('$Format')
                       and self.archive_commit != commit)
        if known_stale: self._commit_count = None
        return known_stale

    def _output_from_file(self, entry='git_describe'):
        """
        Read the version from a .version file that may exist alongside __init__.py.

        This file can be generated by piping the following output to file:

        git describe --long --match v*.*
        """
        try:
            vfile = os.path.join(os.path.dirname(self.fpath), '.version')
            with open(vfile, 'r') as f:
                return json.loads(f.read()).get(entry, None)
        except: # File may be missing if using pip + git archive
            return None


    def _update_from_vcs(self, output):
        "Update state based on the VCS state e.g the output of git describe"
        split = output[1:].split('-')
        dot_split = split[0].split('.')
        for prefix in ['a','b','rc']:
            if prefix in dot_split[-1]:
                prefix_split = dot_split[-1].split(prefix)
                self._prerelease = prefix + prefix_split[-1]
                dot_split[-1] = prefix_split[0]


        self._release = tuple(int(el) for el in dot_split)
        self._commit_count = int(split[1])

        self._commit = str(split[2][1:]) # Strip out 'g' prefix ('g'=>'git')

        self._dirty = (split[-1]=='dirty')
        return self

    def __str__(self):
        """
        Version in x.y.z string format. Does not include the "v"
        prefix of the VCS version tags, for pip compatibility.

        If the commit count is non-zero or the repository is dirty,
        the string representation is equivalent to the output of::

          git describe --long --match v*.* --dirty

        (with "v" prefix removed).
        """
        known_stale = self._known_stale()
        if self.release is None and not known_stale:
            extracted_directory_tag = self._output_from_file(entry='extracted_directory_tag')
            return 'None' if extracted_directory_tag is None else extracted_directory_tag
        elif self.release is None and known_stale:
            extracted_directory_tag = self._output_from_file(entry='extracted_directory_tag')
            if extracted_directory_tag is not None:
                return extracted_directory_tag
            return '0.0.0+g{SHA}-gitarchive'.format(SHA=self.archive_commit)

        release = '.'.join(str(el) for el in self.release)
        prerelease = '' if self.prerelease is None else self.prerelease

        if self.commit_count == 0 and not self.dirty:
            return release + prerelease

        commit = self.commit
        dirty = '-dirty' if self.dirty else ''
        archive_commit = ''
        if known_stale:
            archive_commit = '-gitarchive'
            commit = self.archive_commit

        if archive_commit != '':
            postcount = self.commit_count_prefix + '0'
        elif self.commit_count not in [0, None]:
            postcount = self.commit_count_prefix + str(self.commit_count)
        else:
            postcount = ''

        components = [release, prerelease, postcount,
                      '' if commit is None else '+g' + commit, dirty,
                      archive_commit]
        return ''.join(components)

    def __repr__(self):
        return str(self)

    def abbrev(self):
        """
        Abbreviated string representation of just the release number.
        """
        return '.'.join(str(el) for el in self.release)

    def verify(self, string_version=None):
        """
        Check that the version information is consistent with the VCS
        before doing a release. If supplied with a string version,
        this is also checked against the current version. Should be
        called from setup.py with the declared package version before
        releasing to PyPI.
        """
        if string_version and string_version != str(self):
            raise Exception("Supplied string version does not match current version.")

        if self.dirty:
            raise Exception("Current working directory is dirty.")

        if self.expected_release is not None and self.release != self.expected_release:
            raise Exception("Declared release does not match current release tag.")

        if self.commit_count !=0:
            raise Exception("Please update the VCS version tag before release.")

        if (self._expected_commit is not None
            and not self._expected_commit.startswith( "$Format")):
            raise Exception("Declared release does not match the VCS version tag")



    @classmethod
    def get_setup_version(cls, setup_path, reponame, describe=False,
                          dirty='report', pkgname=None, archive_commit=None):
        """
        Helper for use in setup.py to get the version from the .version file (if available)
        or more up-to-date information from git describe (if available).

        Assumes the __init__.py will be found in the directory
        {reponame}/__init__.py relative to setup.py unless pkgname is
        explicitly specified in which case that name is used instead.

        If describe is True, the raw string obtained from git described is
        returned which is useful for updating the .version file.

        The dirty policy can be one of 'report', 'strip', 'raise'. If it is
        'report' the version string may end in '-dirty' if the repository is
        in a dirty state.  If the policy is 'strip', the '-dirty' suffix
        will be stripped out if present. If the policy is 'raise', an
        exception is raised if the repository is in a dirty state. This can
        be useful if you want to make sure packages are not built from a
        dirty repository state.
        """
        pkgname = reponame if pkgname is None else pkgname
        policies = ['raise','report', 'strip']
        if dirty not in policies:
            raise AssertionError("get_setup_version dirty policy must be in %r" % policies)

        fpath = os.path.join(setup_path, pkgname, "__init__.py")
        version = Version(fpath=fpath, reponame=reponame, archive_commit=archive_commit)
        if describe:
            vstring = version.git_fetch(as_string=True)
        else:
            vstring = str(version)

        if version.dirty and dirty == 'raise':
            raise AssertionError('Repository is in a dirty state.')
        elif version.dirty and dirty=='strip':
            return vstring.replace('-dirty', '')
        else:
            return vstring


    @classmethod
    def extract_directory_tag(cls, setup_path, reponame):
        setup_dir = os.path.split(setup_path)[-1] # Directory containing setup.py
        prefix = reponame + '-' # Prefix to match
        if setup_dir.startswith(prefix):
            tag = setup_dir[len(prefix):]
            # Assuming the tag is a version if it isn't empty, 'master', 'main' and has a dot in it
            if tag not in ['', 'master', 'main'] and ('.' in tag):
                return tag
        return None


    @classmethod
    def setup_version(cls, setup_path, reponame, archive_commit=None,
                      pkgname=None, dirty='report'):
        info = {}
        git_describe = None
        pkgname = reponame if pkgname is None else pkgname
        try:
            # Will only work if in a git repo and git is available
            git_describe  = Version.get_setup_version(setup_path,
                                                      reponame,
                                                      describe=True,
                                                      dirty=dirty,
                                                      pkgname=pkgname,
                                                      archive_commit=archive_commit)

            if git_describe is not None:
                info['git_describe'] = git_describe
        except: pass

        if git_describe is None:
            extracted_directory_tag = Version.extract_directory_tag(setup_path, reponame)
            if extracted_directory_tag is not None:
                info['extracted_directory_tag'] = extracted_directory_tag
            try:
                with open(os.path.join(setup_path, pkgname, '.version'), 'w') as f:
                    f.write(json.dumps({'extracted_directory_tag':extracted_directory_tag}))
            except:
                print('Error in setup_version: could not write .version file.')


        info['version_string'] =  Version.get_setup_version(setup_path,
                                                            reponame,
                                                            describe=False,
                                                            dirty=dirty,
                                                            pkgname=pkgname,
                                                            archive_commit=archive_commit)
        try:
            with open(os.path.join(setup_path, pkgname, '.version'), 'w') as f:
                f.write(json.dumps(info))
        except:
            print('Error in setup_version: could not write .version file.')

        return info['version_string']



def get_setup_version(location, reponame, pkgname=None, archive_commit=None):
    """Helper for use in setup.py to get the current version from either
    git describe or the .version file (if available).

    Set pkgname to the package name if it is different from the
    repository name.

    To ensure git information is included in a git archive, add
    setup.py to .gitattributes (in addition to __init__):
    ```
    __init__.py export-subst
    setup.py export-subst
    ```
    Then supply "$Format:%h$" for archive_commit.

    """
    import warnings
    pkgname = reponame if pkgname is None else pkgname
    if archive_commit is None:
        warnings.warn("No archive commit available; git archives will not contain version information")
    return Version.setup_version(os.path.dirname(os.path.abspath(location)),reponame,pkgname=pkgname,archive_commit=archive_commit)


def get_setupcfg_version():
    """As get_setup_version(), but configure via setup.cfg.

    If your project uses setup.cfg to configure setuptools, and hence has
    at least a "name" key in the [metadata] section, you can
    set the version as follows:
    ```
    [metadata]
    name = mypackage
    version = attr: autover.version.get_setup_version2
    ```

    If the repository name is different from the package name, specify
    `reponame` as a [tool:autover] option:
    ```
    [tool:autover]
    reponame = mypackage
    ```

    To ensure git information is included in a git archive, add
    setup.cfg to .gitattributes (in addition to __init__):
    ```
    __init__.py export-subst
    setup.cfg export-subst
    ```

    Then add the following to setup.cfg:
    ```
    [tool:autover.configparser_workaround.archive_commit=$Format:%h$]
    ```

    The above being a section heading rather than just a key is
    because setuptools requires % to be escaped with %, or it can't
    parse setup.cfg...but then git export-subst would not work.

    """
    try:
        import configparser
    except ImportError:
        import ConfigParser as configparser # python2 (also prevents dict-like access)
    import re
    cfg = "setup.cfg"
    autover_section = 'tool:autover'
    config = configparser.ConfigParser()
    config.read(cfg)
    pkgname = config.get('metadata','name')
    reponame = config.get(autover_section,'reponame',vars={'reponame':pkgname}) if autover_section in config.sections() else pkgname

    ###
    # hack archive_commit into section heading; see docstring
    archive_commit = None
    archive_commit_key = autover_section+'.configparser_workaround.archive_commit'
    for section in config.sections():
        if section.startswith(archive_commit_key):
            archive_commit = re.match(".*=\s*(\S*)\s*",section).group(1)
    ###
    return get_setup_version(cfg,reponame=reponame,pkgname=pkgname,archive_commit=archive_commit)
