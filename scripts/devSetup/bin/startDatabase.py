__author__ = u'schmatz'
from subprocess import call
import os
import sys
import subprocess
#copied straight from the python 3 standard library
def which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode)
                and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if not os.curdir in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if not normdir in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None

#TODO: Upgrade this so it works on windows
#These scripts will be placed in coco/bin

current_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
if which("mongod") and "v2.5.4" in subprocess.check_output("mongod --version",shell=True):
    mongo_executable = "mongod"
else:
    mongo_executable = None
    print("Mongod 2.5.4 wasn't found. Searching in bin directory...")

mongo_directory = current_directory + os.sep + u"mongo"
if not mongo_executable:
    mongo_executable = os.environ.get("COCO_MONGOD_PATH",mongo_directory + os.sep + u"mongod")
    if not os.path.exists(mongo_executable):
        raise FileNotFoundError("Mongo executable not found.")
    print("Using mongo executable: " + str(mongo_executable))
mongo_db_path = os.path.abspath(os.path.join(current_directory,os.pardir)) + os.sep + u"mongo"
if not os.path.exists(mongo_db_path):
    os.mkdir(mongo_db_path)
mongo_arguments = [mongo_executable + u" --setParameter textSearchEnabled=true --dbpath=" + mongo_db_path]
call(mongo_arguments,shell=True)

