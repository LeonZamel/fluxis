#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Add the current directory to the path so that all packages are found. I.e. such that api finds engine
# If there is nicer way to do this, please let me know. This feels like a hack...
sys.path.append(os.getcwd())


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
