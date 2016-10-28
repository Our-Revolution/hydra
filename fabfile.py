from fabric.api import *


def production():
    # todo: make env / variable
    env.hosts = ['ec2-35-161-201-218.us-west-2.compute.amazonaws.com']


def deploy():
    with cd('hydra')
        run('workon hydra')
        run('supervisorctl stop gunicorn')
        run('git pull origin master')
        run('supervisorctl start gunicorn')
        # todo: varnish, etc.