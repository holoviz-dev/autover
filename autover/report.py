from __future__ import print_function
import os.path, importlib, subprocess

def report(*packages):
    """Import and print the library version and filesystem location for
    each Python package or shell command specified.

    """
    for package in packages:
        loc = "not installed in this environment"
        ver = "unknown"

        try:
            module = importlib.import_module(package)
            loc =  os.path.dirname(module.__file__)

            try:
                ver = str(module.__version__)
            except Exception:
                pass

        except ImportError:
            try:
                # See if there is a command by that name and check its --version if so

                # which not usually available on windows, though it
                # could be (e.g. running in some kind of bash for
                # windows, or which binary has been installed,
                # etc...), so try it first. (And -a to match the list
                # you get from where; might want to report more than
                # one in the future if investigating confusion over
                # what command runs when someone types 'command'.)
                try:
                    loc = subprocess.check_output(['which','-a',      package]).decode().splitlines()[0].strip()
                except:
                    # .exe in case powershell (otherwise wouldn't need it)
                    loc = subprocess.check_output(['where.exe',       package]).decode().splitlines()[0].strip()

                out = ""
                try:
                    out = subprocess.check_output([package, '--version'], stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    out = e.output

                # Assume first word in output with a period and digits is the version
                for s in out.decode().split():
                    if '.' in s and sum(str.isdigit(c) for c in s)>=2:
                        ver=s.strip()
                        break
            except Exception as e:
                pass

        print("{0:30} # {1}".format(package + "=" + ver,loc))
