# coding=utf-8
import os

from fabric import task
from fabric import Connection
from patchwork.transfers import rsync
from invoke.context import Context

key_filename = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
host = 'xxx.xxx.xxx.xxx'
user = '{{ project_name }}'
port = 2020
project_root = '~/app'


def update_config(connect):
    '''
    Заполняем параметры подключения
    '''
    # Если в параметрах запуска не задан хост, то тут тип Context
    if isinstance(connect, Context):
        connect = Connection(host=host)  # Инициализируем Connection
    conf = {
        "user": user,
        "port": port,
        "connect_kwargs": {"key_filename": key_filename},
    }
    for k, v in conf.items():
        if hasattr(connect, k):
            setattr(connect, k, v)
    return connect


@task
def build(connect_obj, only=False):
    '''
    Локальная сборка проекта
    '''
    if not only or only == 'app':
        with update_config(connect_obj) as c:
            c.local('docker build -f docker/production/Dockerfile \
                -t {{ project_name }}/projects:{{ project_name }}-app .')
            c.local('docker login')
            c.local('docker push {{ project_name }}/projects:{{ project_name }}-app')

@task
def deploy(connect_obj):
    '''
    Резвёртывание проекта на сервере
    '''
    with update_config(connect_obj) as c:
        with c.cd(project_root):
            # run('git pull origin master')
            c.put('docker/production/docker-compose.yml', 'app/')

            c.run('docker-compose pull')
            c.run('docker-compose up -d')


@task
def build_deploy(connect_obj, only=False):
    '''
    Локальная сборка и развёртывание на сервере
    '''
    build(connect_obj, only)
    deploy(connect_obj)


@task
def clear_cache(connect_obj):
    '''
    Очистка кэша Django на сервере
    '''
    with update_config(connect_obj) as c:
        with c.cd(project_root):
            c.run('docker-compose exec --rm manage clear_cache')


@task
def restart(connect_obj):
    '''
    Перезапуск докер на сервере
    '''
    with update_config(connect_obj) as c:
        with c.cd(project_root):
            c.run('docker-compose restart')


@task
def clear_containers(connect_obj):
    '''
    Удалить неиспользуемые контейнеры на сервере
    '''
    with update_config(connect_obj) as c:
        with c.cd(project_root):
            c.run('docker system prune -a')


if __name__ == '__main__':
    server = Connection(host=host)
    build_deploy(server)
