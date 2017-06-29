import sys
from time import time

from humanfriendly import format_timespan


class Timer(object):
    r"""Print the elapsed time after the execution of a block of code.
    """

    def __init__(self, desc='Running...', disable=False):
        self._disable = disable
        self._tstart = None
        self._desc = desc
        self.elapsed = None

    def __enter__(self):
        self._tstart = time()
        if not self._disable:
            sys.stdout.write(self._desc)
            sys.stdout.flush()
        return self

    def __exit__(self, type_, value_, traceback_):
        self.elapsed = time() - self._tstart
        if not self._disable:
            print(" done (%s)." % format_timespan(self.elapsed))
            sys.stdout.flush()
