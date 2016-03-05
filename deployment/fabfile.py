import os.path

from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import sudo
from fabric.api import local
from fabric.context_managers import shell_env


env.use_ssh_config = True


def update_source():
    with cd('source'):
        branch = 'dev' if env.host == 'localhost' else 'master'
        run('git checkout ' + branch)
        run('git fetch')
        current_commit = local('git log {branch} -n 1 --format=%H'.format(branch=branch), capture=True)
        run('git reset --hard ' + current_commit)


def update_virtualenv():
    run('venv/bin/pip install -r source/requirements.txt')


def restart_gunicorn_server():
    sudo('supervisorctl restart gunicorn')


def refresh_redis():
    app_dir = os.path.join('sites', env.host, 'source', 'app')
    with cd(app_dir):
        run('../../venv/bin/python -c "import bus_stop; bus_stop.import_map_to_redis()"')


def deploy():
    site_dir = os.path.join('sites', env.host)
    with cd(site_dir):
        update_source()
        update_virtualenv()
    restart_gunicorn_server()


def update_gunicorn_config():
    deploy_dir = os.path.join('sites', env.host, 'source', 'deployment')
    with cd(deploy_dir):
        with shell_env(SITENAME=env.host):
            run("sed -e s/'$SITENAME'/$SITENAME/g gunicorn_start_template.sh > gunicorn_start.sh")