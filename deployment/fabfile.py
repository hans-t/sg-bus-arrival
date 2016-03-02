from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import sudo
from fabric.api import local


def update_source():
    with cd('source'):
        run('git fetch')
        current_commit = local('git log -n 1 --format=%H', capture=True)
        run('git reset --hard {}'.format(current_commit))


def update_virtualenv():
    run('venv/bin/pip install -r source/requirements.txt')


def restart_gunicorn_server():
    sudo('supervisorctl restart gunicorn')


def deploy():
    site_dir = 'sites/{sitename}/'.format(sitename=env.host)
    with cd(site_dir):
        update_source()
        update_virtualenv()
    restart_gunicorn_server()