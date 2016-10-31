from fabric.api import *


def production():
    # todo: make env / variable
    # todo: make ELB friendly
    env.hosts = ['ec2-35-161-201-218.us-west-2.compute.amazonaws.com', 'ec2-35-161-228-190.us-west-2.compute.amazonaws.com']
    env.forward_agent = True
    env.key_filename = '~/.ssh/hydra.pem'
    env.user = 'ubuntu'


def deploy():
    with cd('hydra'):
        with prefix('source $(which virtualenvwrapper.sh)'):
            with prefix('workon hydra'):
                run('supervisorctl stop gunicorn')
                run('git pull origin master')
                run('supervisorctl start gunicorn')
            # todo: varnish, etc.