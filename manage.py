#!/usr/bin/env python
<<<<<<< HEAD
"""Django's command-line utility for administrative tasks."""
=======
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
import os
import sys


def main():
<<<<<<< HEAD
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
=======
    """Run administrativo"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenda_project.settings')
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
