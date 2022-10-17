# Configuration file for jupyterhub.
# Note: As we use jupyterhub/jupyterhub-onbuild, this file will automatically copied into
# the jupyterhub image at docker-compose build

import os

c = get_config()

network_name = 'jupyterhub-network'
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
c.DockerSpawner.extra_host_config = {'network_mode': network_name}

c.Authenticator.admin_users = {'test2', 'admin'}
c.Authenticator.delete_invalid_users = True
c.Authenticator

# import tornado.gen as gen
# from jupyterhub.auth import DummyAuthenticator
# class MyDummyAuthenticator(DummyAuthenticator):
#     @gen.coroutine
#     def pre_spawn_start(self, user, spawner):
#         spawner.environment['NB_USER'] = spawner.environment['JUPYTERHUB_USER'] # doesn't work
#
# c.JupyterHub.authenticator_class = MyDummyAuthenticator

# does't work
# from subprocess import check_call
# def my_hook(spawner):
#     username = spawner.user.name
#     spawner.environment['NB_USER'] = username
#     #check_call(['./examples/bootstrap-script/bootstrap.sh', username])
# c.Spawner.pre_spawn_hook = my_hook

c.JupyterHub.authenticator_class = "dummy"
c.DummyAuthenticator.password = "dd"

c.JupyterHub.default_server_name = 'miek'
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

c.DockerSpawner.remove = True

# JupyterHub requires a single-user instance of the Notebook server, so we default to using
# the `start-singleuser.sh` script included in the jupyter/docker-stacks *-notebook images as
# the Docker run command when spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
# c.DockerSpawner.image = 'jupyter/minimal-notebook:hub-3.0.0'
c.DockerSpawner.image = 'dh_test:latest'
#c.DockerSpawner.extra_create_kwargs.update({'command': "start-singleuser.sh"})
c.DockerSpawner.cmd = ['start.sh', 'jupyterhub-singleuser', '--allow-root']
c.DockerSpawner.post_start_cmd = "bash /home/post_start.sh"

#
#
# c.DockerSpawner.environment = {
#     #'NB_USER': 'tete',
#     #'NB_USER': '{USER}',  # close. puts '{USER}' in all the right places
# #     'NB_USER': '${JUPYTERHUB_USER}',  # whoami is correct, but still /home/{JUPYTERHUB_USER}
# #     #'NB_USER': '$JUPYTERHUB_USER', # whoami is correct, but still /home/$JUPYTERHUB_USER
# }
# #c.DockerSpawner.args =["NB_USER={username}"]
c.DockerSpawner.Spawner.post_start_cmd = 'bash -c export test123=fff'


# suggestion from https://jupyterhub.readthedocs.io/en/stable/api/spawner.html#jupyterhub.spawner.Spawner.default_url
#c.Spawner.notebook_dir = '/home/${JUPYTERHUB_USER}'
c.Spawner.default_url = '/tree'

# Mount the real user's Docker volume on the host to the notebook user's notebook directory in the container
notebook_dir = '/home/{username}'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {'jupyterhub-user-{username}': notebook_dir }


def create_dir_hook(spawner):
    username = spawner.user.name  # get the username
    volume_path = os.path.join('/home', username)
    if not os.path.exists(volume_path):
        # create a directory with umask 0755
        # hub and container user must have the same UID to be writeable
        # still readable by other users on the system
        os.mkdir(volume_path, 0o755)

        # spawner.environment['NB_UID'] = 1000
        # spawner.environment['NB_GID'] = 100
        # spawner.environment['GRANT_SUDO'] = 'yes'



# attach the hook function to the spawner
#c.Spawner.pre_spawn_hook = create_dir_hook

# c.DockerSpawner.allowed_images = {
#   'Jupyter':'jupyterhub/singleuser:3',
#   'JupyterDH':'dh_proxy:latest',
#   'JupyterDH2':'dh_proxy2:latest',
#   'JupyterDH3':'dh_proxy3:latest',
#  # 'Deephaven':'ghcr.io/deephaven/server:0.17.0',
# }
