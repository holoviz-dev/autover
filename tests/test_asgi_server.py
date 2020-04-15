import autover
from starlette.applications import Starlette

# A simple ASGI server application
# that tries to make use of autover.
#
# Given that autover makes use of
# subprocess.Popen and the program
# workflow depends on that, there
# were some corner cases where
# autover would just crash if we
# tried to get its __version__,
# therefore crashing the whole
# ASGI application.
#
# This test application is used
# with Gunicorn in the unit tests
# (testversion.py), just to check
# if the ASGI application crashes
# or not.

_ = autover.__version__

app = Starlette()
