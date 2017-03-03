""" Deployment Scripts for pupgetshingsdone.com 

TODO: Replace with https://github.com/tomerfiliba/plumbum
"""
# pylint: skip-file

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/cdcarter/pupgetsthingsdone.com.git"


def deploy():
    """ Deploy pupgetsthingsdone with gunicorn and nginx. """

    site_folder = '/home/{0}/sites/{1}'.format(env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def destroy():
    """ DANGER! Destroys the site """
    run('rm -rf /home/{0}/sites/{1}'.format(env.user, env.host))


def _create_directory_structure_if_necessary(site_folder):
    for d in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p {base}/{sub}'.format(base=site_folder, sub=d))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(
        'cd {0} && '.format(source_folder) +
        'git reset --hard {0}'.format(current_commit)
    )


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(
        settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{}"]'.format(site_name)
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('python3.6 -m venv {0}'.format(virtualenv_folder))

    run('{0}/bin/pip install -r {1}/requirements.txt'.format(
        virtualenv_folder,
        source_folder
    ))


def _update_static_files(source_folder):
    run(
        'cd {0} && '.format(source_folder) +
        '../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    run(
        'cd {0} && '.format(source_folder) +
        '../virtualenv/bin/python manage.py migrate --noinput'
    )
