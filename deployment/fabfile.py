import os.path

from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import sudo
from fabric.api import local
from fabric.context_managers import shell_env


env.use_ssh_config = True
ROOT_DIR = os.path.join(os.path.expanduser('~'), 'sites', '{host}')
SOURCE_DIR = os.path.join(ROOT_DIR, 'source')
APP_DIR = os.path.join(SOURCE_DIR, 'app')
DEPLOY_DIR = os.path.join(SOURCE_DIR, 'deployment')


def update_source():
    with cd(SOURCE_DIR.format(**env)):
        branch = 'dev' if env.host == 'localhost' else 'master'
        run('git checkout ' + branch)
        run('git fetch')
        current_commit = local('git log {branch} -n 1 --format=%H'.format(branch=branch), capture=True)
        run('git reset --hard ' + current_commit)


def update_virtualenv():
    with cd(ROOT_DIR.format(**env)):
        run('venv/bin/pip install -r source/requirements.txt')


def restart_gunicorn_server():
    sudo('supervisorctl restart gunicorn')


def refresh_redis():
    with cd(APP_DIR.format(**env)):
        run('../../venv/bin/python -c "import bus_stop; bus_stop.import_map_to_redis()"')


def deploy():
    update_source()
    update_virtualenv()
    restart_gunicorn_server()


def update_gunicorn_config():
    with cd(DEPLOY_DIR.format(**env)):
        with shell_env(SITENAME=env.host):
            run("sed -e s/'$SITENAME'/$SITENAME/g gunicorn_start_template.sh > gunicorn_start.sh")


def update_nginx_config():
    with cd(DEPLOY_DIR.format(**env)):
        with shell_env(SITENAME=env.host, ROOT=ROOT_DIR.format(**env), DOLLAR='$'):
            run('envsubst < nginx_template.conf > nginx-$SITENAME.conf')
            sudo('cp nginx-$SITENAME.conf /etc/nginx/sites-available/$SITENAME.conf')
    sudo('service nginx reload')