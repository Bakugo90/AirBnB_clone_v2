#!/usr/bin/python3
from datetime import datetime
from fabric.api import *
from os import path


env.hosts = ['35.229.93.37', '54.196.213.127']


@runs_once
def do_pack():
    """Generates a .tgz archive from the contents
    of the web_static folder of this repository.
    """

    d = datetime.now()
    now = d.strftime('%Y%m%d%H%M%S')
    path = "versions/web_static_{}.tgz".format(now)

    local("mkdir -p versions")
    local("tar -czvf {} web_static".format(path))
    return path


def do_deploy(archive_path):
    """Distributes a .tgz archive through web servers
    """

    if path.exists(archive_path):
        archive = archive_path.split('/')[1]
        a_path = "/tmp/{}".format(archive)
        folder = archive.split('.')[0]
        f_path = "/data/web_static/releases/{}/".format(folder)

        put(archive_path, a_path)
        run("mkdir -p {}".format(f_path))
        run("tar -xzf {} -C {}".format(a_path, f_path))
        run("rm {}".format(a_path))
        run("mv -f {}web_static/* {}".format(f_path, f_path))
        run("rm -rf {}web_static".format(f_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(f_path))

        return True

    return False


def gets_out_of_date(number, _type):
    """Gets a number of content that is out of date
    """

    if number == 0:
        number = 1

    if _type == 'local':
        content = local("ls -td web_static_*", capture=True)
    elif _type == 'remote':
        content = run("ls -td web_static_*")

    content_list = content.split()
    out_of_date = content_list[number:]
    return out_of_date


def do_clean(number=0):
    """Deletes out-of-date .tgz archives of web servers
    """

    number = int(number)

    if number >= 0:
        with lcd("versions"):
            _files = gets_out_of_date(number, 'local')

            for _file in _files:
                local("rm -f {file}".format(file=_file))

        with cd("/data/web_static/releases"):
            _folders = gets_out_of_date(number, 'remote')

            for _folder in _folders:
                run("rm -rf {folder}".format(folder=_folder))


def deploy():
    """Creates and Distributes a .tgz archive through web servers
    """

    archive = do_pack()
    return do_deploy(archive)
