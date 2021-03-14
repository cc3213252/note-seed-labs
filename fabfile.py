# coding=utf8

from fabric.api import *
from fabric.contrib.project import rsync_project

dev_host = 'www@www.blueegg.net.cn'


def upload(remote_dir):
    local_dir = './site/'
    if local_dir[-1] != '/':
        local_dir += '/'
    rsync_project(local_dir=local_dir, remote_dir=remote_dir, delete=True)


@task
@hosts([dev_host])
def dev_upload():
    remote_dir = '/home/www/note.blueegg.net.cn/seed-labs'
    upload(remote_dir)


# fab dev_upload
