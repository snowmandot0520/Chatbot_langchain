#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess


def main():
    # Run npm build command first
    if os.name == 'nt':
        npm_install = subprocess.Popen(["npm", "install"], cwd="client/", shell=True)
        npm_build = subprocess.Popen(["npm", "run", "build"], cwd="client/", shell=True)
    else:
        npm_install = subprocess.Popen(["npm", "install"], cwd="client/")
        npm_build = subprocess.Popen(["npm", "run", "build"], cwd="client/")
    npm_install.wait()  # Wait for npm install to finish
    npm_build.wait()  # Wait for npm build to finish
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
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
    main()
