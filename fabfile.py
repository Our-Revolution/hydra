from fabric.api import *


def production():
    # todo: make env / variable
    # todo: make ELB friendly
    env.hosts = ['ec2-35-161-201-218.us-west-2.compute.amazonaws.com', 'ec2-35-161-228-190.us-west-2.compute.amazonaws.com']
    env.forward_agent = True
    env.key_filename = '~/.ssh/hydra.pem'
    env.user = 'ubuntu'


def deploy(pip_install=False, migrate=False):

    with cd('hydra'):
        with prefix('source $(which virtualenvwrapper.sh)'):
            with prefix('workon hydra'):
                run('supervisorctl stop gunicorn')
                run('git pull origin master')

                run('./manage.py collectstatic --noinput')

                if str(pip_install).lower() == 'true':
                    run('pip install -r requirements.txt')

                if str(migrate).lower() == 'true':
                    run('./manage.py migrate')

                run('supervisorctl start gunicorn')
            # todo: varnish, etc.


def restart_gunicorn():

    with cd('hydra'):
        with prefix('source $(which virtualenvwrapper.sh)'):
            with prefix('workon hydra'):
                run('supervisorctl restart gunicorn')


def config_set(**kwargs):
    if not kwargs:
        print "kwargs empty! Pass in a variable you want to set"
        print "e.g.: fab production config_set:DOUBLE_SECRET_PASSWORD=\"yolo\""
        exit(1)

    # this is going to get untenable... use with discretion!
    with cd('/home/ubuntu/.virtualenvs/hydra/bin'):
        for key, value in kwargs.iteritems():
            run('echo "\nexport %s=%s" >> activate' % (key, value))

    with cd('hydra'):
        with prefix('source $(which virtualenvwrapper.sh)'):
            with prefix('workon hydra'):
                # manually stop gunicorn
                run('supervisorctl stop gunicorn')
                run('cat supervisord.pid | xargs kill')
                run('supervisord')
                run('supervisorctl reload')
                run('supervisorctl start gunicorn')