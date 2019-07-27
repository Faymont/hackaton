#!/usr/local/bin/python
import sys
import signal

from django.core.management import execute_from_command_line


def sighandler(signum, frame):
    sys.exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sighandler)
    signal.signal(signal.SIGINT, sighandler)
    execute_from_command_line(sys.argv)
