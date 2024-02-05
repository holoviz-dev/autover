# TODO:
# - tmp dirs

import os

import doit
from doit import action

from pyct import *  # noqa

############################################################
# TODO: remove if project is updated to use pyctdev
miniconda_url = {
    "Windows": "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe",
    "Linux": "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh",
    "Darwin": "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
}
def task_download_miniconda():
    import platform

    try:
        from urllib.request import urlretrieve
    except ImportError:
        from urllib import urlretrieve
    
    url = miniconda_url[platform.system()]
    miniconda_installer = url.split('/')[-1]

    def download_miniconda(targets):
        urlretrieve(url,miniconda_installer)

    return {'targets': [miniconda_installer],
            'uptodate': [True], # (as has no deps)
            'actions': [download_miniconda]}
############################################################

example = {
    'name':'example',
    'long':'example',
    'type':str,
    'default':'pkg_depend'
}

example_pkgname = {
    'name':'example_pkgname',
    'long':'example-pkgname',
    'type':str,
    'default':''
}

from distutils.dir_util import copy_tree

def task_copy_example_project():
    def copy_example(example):
        from_ = os.path.join(doit.get_initial_workdir(), "examples", example)
        copy_tree(from_,'.')

    return {
        'params':[example],
        'actions':[(copy_example,),]
    }


def task_git_init():
    return {
        'actions':[
            action.CmdAction('git init && git add . && git commit -m "init" && git tag -a v0.0.1 -m "one" && echo two > two && git add two && git commit -m "two"')
        ]
    }


def task_get_git_version():
    return {'actions': [action.CmdAction('git describe --long',save_out='git_version')]}


def _x(example,example_pkgname):
    # more param computing :(
    return example_pkgname if example_pkgname!='' else example


# TODO: this task - like develop install below - should be done in a
# throwaway environment. Should probably just use tox here too.

def task_verify_installed_version():
    return {
        'getargs': {'git_version': ('get_git_version','git_version')},
        'uptodate': [False],
        'params': [example,example_pkgname],
        'actions':[
            action.CmdAction(
                lambda example,example_pkgname: 'mkdir /tmp/9k && cd /tmp/9k && tmpverify %s'%_x(example,example_pkgname) +' %(git_version)s'),
        ]
    }


# TODO: split up
def task_original_script():
    env1 = os.environ.copy()
    shared_packages = os.path.join(doit.get_initial_workdir(), "dist")
    env1["PIP_FIND_LINKS"] = shared_packages

    env2 = os.environ.copy()
    env2['PYTHONPATH'] = os.getcwd() # TODO win

    def record_pkg_bundle_version(example,example_pkgname):
        pkgname = _x(example,example_pkgname)
        return ("""python -c 'import os; from version import Version;"""
                + ('print("Writing .version for %s in %s");' % (example_pkgname, example))
                + """Version.record_version(os.getcwd(), """ + "\"%s\"" % pkgname + """, archive_commit="$Format:%%h$")'""")

    def record_pkg_skip(example,example_pkgname):
        return """python -c 'print(\"Not recording .version\")'"""

    def remove_version_file(example,example_pkgname):
        pkgname = _x(example,example_pkgname)
        return (("rm ./%s/.version" % pkgname)
                if pkgname in ['pkg_bundle', 'PkgBundle']
                else ("echo 'Skipping removal of .version for %s in %s'"
                      % (example_pkgname, example)))


    record_mapping={'pkg_bundle':record_pkg_bundle_version,
                    'PkgBundle': record_pkg_bundle_version}
    return {
        'getargs': {'git_version': ('get_git_version','git_version')},
        'params': [example,example_pkgname],
        'actions':[
            # 0. Create .version file for tox
            action.CmdAction(lambda example,example_pkgname: record_mapping.get(_x(example,example_pkgname),record_pkg_skip)(example,example_pkgname),
                             env=env1),
            # 1. verify package generation & installation
            action.CmdAction('tox -e py -- %(git_version)s',env=env1),
            # 2. Remove .version file
            action.CmdAction(remove_version_file, env=env1),

            # dev install, then...
            # TODO: need prerelease param just now; remove pre & index urls after release
            action.CmdAction('pip install -f ' + shared_packages + ' --pre --index-url=https://test.pypi.org/simple/ --extra-index-url=https://pypi.org/simple -e .',env=env2),

            # 2. ...verify in git repo (TODO: could just be "tmpverify %(example)s", I think)
            action.CmdAction(lambda example,example_pkgname: 'python '+ _x(example,example_pkgname)+'/tests/__init__.py '+_x(example,example_pkgname),env=env2),
            # 3. ...verify outside git repo
            action.CmdAction(lambda example,example_pkgname: 'mkdir /tmp/9k && cd /tmp/9k && tmpverify '+_x(example,example_pkgname) +' %(git_version)s',env=env2),

            # TODO: should be some kind of clean up option
            action.CmdAction(lambda example,example_pkgname: 'pip uninstall -y '+_x(example,example_pkgname))
        ]
    }

def task_check_dirty_package_name():
    # TODO: test should be less bash
    return {
        'actions':[
            'echo "#dirty" >> setup.py',
            'git describe --dirty --long',
            'python setup.py sdist',
            'python -c "import os,glob; assert len(glob.glob(\'dist/*+g*.dirty.tar.gz\'))==1, os.listdir(\'dist\')"',
        ]}

def task_check_dirty_fails_conda_package():
    # TODO: test should be less bash
    return {
        'actions':[
            'echo "#dirty" >> setup.py',
            'git describe --dirty --long',
            '! conda build conda.recipe > conda-dirty-check 2>&1',
            'grep "Error: bad character \'-\' in package/version" conda-dirty-check'
        ],
        'teardown':[
            'python -c "print(open(\'conda-dirty-check\').read())"'
        ]}
