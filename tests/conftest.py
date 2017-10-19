# -*- coding: utf-8 -*-

import os
import uuid
import shutil
import hashlib
import tempfile

import pytest

import multidl.downloaders


@pytest.fixture(scope='session')
def http_url():
    return (
        'http://ovh.net/files/1Mio.dat',
        hashlib.sha1,
        '22c952ea2b497171d37b76f0830ef8d9911cfe9b',
        1048576,
    )


@pytest.fixture(scope='session')
def ftp_url():
    return (
        'ftp://speedtest.tele2.net/1MB.zip',
        hashlib.sha1,
        '3b71f43ff30f4b15b5cd85dd9e95ebc7e84eb5a3',
        1048576,
    )


@pytest.fixture(scope='session')
def local_file_url():
    filename = str(uuid.uuid4())
    content = str(uuid.uuid4()).encode('utf-8')
    content_hash = hashlib.sha1(content).hexdigest()
    with open(filename, 'wb') as f:
        f.write(content)

    yield (
        'file://' + os.path.abspath(filename),
        hashlib.sha1,
        content_hash,
        len(content),
    )

    os.remove(filename)


@pytest.fixture(scope='session')
def test_urls(http_url, ftp_url, local_file_url):
    return [
        http_url,
        ftp_url,
        local_file_url,
    ]


@pytest.fixture(scope='function')
def tempdir():
    base_tempdir = tempfile.gettempdir()
    random = str(uuid.uuid4())
    resulting_tempdir = os.path.join(base_tempdir, random)

    os.makedirs(resulting_tempdir)

    yield resulting_tempdir

    shutil.rmtree(resulting_tempdir, ignore_errors=True)


@pytest.fixture(
    params=[
        ('http_url', multidl.downloaders.HttpDownloader),
        ('ftp_url', multidl.downloaders.FtpDownloader),
        ('local_file_url', multidl.downloaders.LocalFileDownloader),
    ]
)
def downloader(request):
    return request.getfixturevalue(request.param[0]), request.param[1]


@pytest.fixture(scope='session')
def config_file(test_urls):

    config_file_name = str(uuid.uuid4())

    with open(config_file_name, 'w') as f:
        for url in test_urls:
            url, _, _, _ = url
            f.write(url + '\n')

    yield os.path.abspath(config_file_name)

    os.remove(config_file_name)
