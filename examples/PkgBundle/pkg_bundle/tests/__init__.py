import sys
import pkg_resources._vendor.packaging.version as packaging_version
import subprocess
import os


def main():

    module_name = sys.argv[1]
    module = __import__(module_name)

    ###############
    # (a) pep440 compliant?
    packaging_version.Version(module.__version__)

    ###############
    # (b) following desired 'latest master' version scheme?
    # v0.2.0-5-g85da374 --> 0.2.0.post5+g85da374

    if len(sys.argv)==5:
        v=sys.argv[2]
        commits=sys.argv[3]
        sha=sys.argv[4]
        print("Git info supplied: %s %s %s"%(v,commits,sha))
    elif len(sys.argv)==3:
        v,commits,sha=sys.argv[2].split('-')
        print("Git info supplied: %s %s %s"%(v,commits,sha))
    elif len(sys.argv)==2:
        desc=subprocess.check_output(['git','describe','--long']).decode('utf8').strip()
        v,commits,sha=desc.split('-')
        print("Git info collected from git in %s: %s %s %s"%(os.getcwd(),v,commits,sha))
    else:
        raise ValueError

    expected_version=v[1::]
    if int(commits) > 0:
        expected_version += '.post'+commits+"+"+sha;

    assert module.__version__ == expected_version, '%s.__version__ %r does not match %r' % (module_name,module.__version__,expected_version)

    ###############
    # (c) setup.py version matches __version__ (only relevant in a source dir)
    if os.path.exists("setup.py"):
        print(os.getcwd())
        print(sys.path)
        try:
            import setup
        except ImportError:
            print("skipping setup.py check")
            import traceback
            traceback.print_exc()
        else:
            print(setup.__file__)
            assert module.__version__ == setup.setup_args['version'], '%s.__version__ %r does not match setup version %r'%(module_name,module.__version__, setup.setup_args['version'])
    else:
        print("No setup.py in %s; skipping test."%os.getcwd())

if __name__ == "__main__":
    main()

