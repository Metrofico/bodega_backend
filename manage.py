#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading

from django.conf import settings


def local_path():
    return os.path.abspath(os.path.dirname(__file__))


def db_files_path():
    return os.path.join(local_path(), settings.DB_FILES_STATIC)


def db_bodega_path():
    return os.path.join(db_files_path(), settings.BODEGA_FOLDER)


def db_bodega_file_path(file):
    return os.path.join(db_bodega_path(), file)


def create_folders_if_not_exist():
    bodega = "./" + settings.DB_FILES_STATIC + "/" + settings.BODEGA_FOLDER
    try:
        os.makedirs(bodega)
        print("Creando directorio: ", str(bodega))
    except FileExistsError:
        # directory already exists
        pass


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodega_backend.settings')
    create_folders_if_not_exist()
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
