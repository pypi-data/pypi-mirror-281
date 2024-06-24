#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Dev Team (https://sequana.readthedocs.io)
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  Website:       https://github.com/sequana/sequana
#  Documentation: http://sequana.readthedocs.io
#  Contributors:  https://github.com/sequana/sequana/graphs/contributors
##############################################################################
import hashlib
import sys

from sequana_pipetools import get_package_version

__all__ = ["Colors", "print_version", "error", "url2hash"]


def url2hash(url):
    md5hash = hashlib.md5()
    md5hash.update(url.encode())
    return md5hash.hexdigest()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Colors:
    """

    ::

        color = Colors()
        print(color.failed("msg"))

    """

    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def failed(self, msg):
        return self.FAIL + msg + self.ENDC

    def bold(self, msg):
        return self.BOLD + msg + self.ENDC

    def purple(self, msg):
        return self.PURPLE + msg + self.ENDC

    def underlined(self, msg):
        return self.UNDERLINE + msg + self.ENDC

    def fail(self, msg):
        return self.FAIL + msg + self.ENDC

    def error(self, msg):
        return self.FAIL + msg + self.ENDC

    def warning(self, msg):
        return self.WARNING + msg + self.ENDC

    def green(self, msg):
        return self.GREEN + msg + self.ENDC

    def blue(self, msg):
        return self.BLUE + msg + self.ENDC


def error(msg, pipeline):
    color = Colors()
    print(color.error("ERROR [sequana.{}]::".format(pipeline) + msg), flush=True)
    sys.exit(1)


def print_version(name):
    try:
        ver = get_package_version(f"sequana_{name}")
        print(f"sequana_{name} version: {ver}")
    except Exception as err:  # pragma: no cover
        print(err)
        print(f"sequana_{name} version: ?")

    try:
        version = get_package_version("sequana")
        print(f"Sequana version: {version}")
    except Exception:  # pragma: no cover
        print(f"Sequana version: not found")

    try:
        version = get_package_version("sequana_pipetools")
        print(f"Sequana_pipetools version: {version}")
    except Exception as err:  # pragma: no cover
        print(err)
        print("Sequana_pipetools version: not found")

    print(Colors().purple("\nHow to help ?\n- Please, consider citing us (see sequana.readthedocs.io)"))
    print(Colors().purple("- Contribute to the code or documentation"))
    print(Colors().purple("- Fill issues on https://github.com/sequana/sequana/issues/new/choose"))
    print(Colors().purple("- Star us https://github.com/sequana/sequana/stargazers"))


class PipetoolsException(Exception):
    pass
