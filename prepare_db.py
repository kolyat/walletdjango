# Copyright (c) 2022 Kirill 'Kolyat' Kiselnikov
# This file is the part of testutils, released under modified MIT license

import os
import shutil

from django.core import management


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'walletdjango.settings')
APPS = ('wallet',)


class Db(object):
    """This class is used for operations with database and migrations, and to
    prepare database with predefined testing data
    """
    def __init__(self, db_info, project_root):
        """
        :param db_info: dict with database settings
        :param project_root: root directory of the project
        """
        self.db_info = db_info
        self.project_root = project_root
        if 'postgresql' in self.db_info['ENGINE']:
            import psycopg2
            self.connection = psycopg2.connect(
                user=db_info['USER'], password=db_info['PASSWORD'],
                host=db_info['HOST'], port=db_info['PORT']
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        else:
            from django.db import connection
            self.connection = connection
            self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def create(self):
        """Database re-creation procedures
        """
        if 'sqlite' in self.db_info['ENGINE']:
            print('Re-creating SQLite database file "{}"...'
                  ''.format(self.db_info['NAME']), end=' ', flush=True)
            open(self.db_info['NAME'], mode='w').close()
            print('OK')
        else:
            print('Deleting database "{}"...'.format(self.db_info['NAME']),
                  end=' ', flush=True)
            self.cursor.execute('DROP DATABASE IF EXISTS {}'
                                ''.format(self.db_info['NAME']))
            print('OK')
            print('Re-creating database...', end=' ', flush=True)
            self.cursor.execute('CREATE DATABASE {} WITH ENCODING \'UTF8\''
                                ''.format(self.db_info['NAME']))
            print('OK')

    def remove_migrations(self, app):
        """Re-create migration directory of project's application

        :param app: application name
        """
        print('Re-creating migration directory for {}...'.format(app),
              end=' ', flush=True)
        _dir = os.path.join(self.project_root, app, 'migrations')
        if os.path.exists(_dir):
            shutil.rmtree(_dir)
        os.mkdir(_dir)
        open(os.path.join(_dir, '__init__.py'), 'w').close()
        print('OK')

    @staticmethod
    def make_migrations(app):
        """Make migrations for project's application

        :param app: application name
        """
        management.call_command('makemigrations', app)

    @staticmethod
    def migrate(*args):
        """Start migration procedure

        :param args: _optional_ name of application
        """
        management.call_command('migrate', *args)

    @staticmethod
    def clear(app):
        """Remove any data from database related to specified application

        :param app: application name
        """
        management.call_command('clear_db_{}'.format(app))

    @staticmethod
    def populate(app):
        """Populate database with predefined testing data related to specified
        application

        :param app: application name
        """
        management.call_command('populate_db_{}'.format(app))


if __name__ == '__main__':
    import django
    django.setup()
    from django.conf import settings
    db = Db(settings.DATABASES['default'], settings.BASE_DIR)
    db.create()
    for a in APPS:
        db.remove_migrations(a)
    for a in APPS:
        db.make_migrations(a)
    db.migrate()
    for a in APPS:
        db.populate(a)
    db.close()
