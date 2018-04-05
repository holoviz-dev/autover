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

        except (ImportError, ModuleNotFoundError):
            try:
                # See if there is a command by that name and check its --version if so
                loc = subprocess.check_output(['which', package]).decode().strip()
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
