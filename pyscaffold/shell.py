# -*- coding: utf-8 -*-
"""
Shell commands like git, django-admin.py etc.
"""

from __future__ import print_function, absolute_import, division

import os
import sys
import functools
import subprocess

__author__ = "Florian Wilhelm"
__copyright__ = "Blue Yonder"
__license__ = "new BSD"


class Command(object):
    """
    Shell command that can be called with flags like git('add', 'file')

    :param command: command to handle
    """
    def __init__(self, command):
        self._command = command

    def __call__(self, *args):
        command = "{cmd} {args}".format(cmd=self._command,
                                        args=subprocess.list2cmdline(args))
        output = subprocess.check_output(command,
                                         shell=True,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
        return self._yield_output(output)

    def _yield_output(self, msg):
        for line in msg.splitlines():
            yield line


def called_process_error2exit_decorator(func):
    """
    Decorator to convert given CalledProcessError to an exit message

    This avoids displaying nasty stack traces to end-users
    """
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except subprocess.CalledProcessError as e:
            print("{err}:{linesep}{msg}".format(err=str(e),
                                                linesep=os.linesep,
                                                msg=e.output))
            sys.exit(1)
    return func_wrapper


#: Command for git
git = Command("git")

#: Command for django-admin.py
django_admin = Command("django-admin.py")