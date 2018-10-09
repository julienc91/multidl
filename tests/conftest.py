# -*- coding: utf-8 -*-

import os
import uuid
import hashlib

import pytest

import multidl.downloaders


def pytest_addoption(parser):
    parser.addoption("--full", action="store_true",
                     help="Run tests based on external resources as well")


def pytest_runtest_setup(item):
    if 'full' in item.keywords and not item.config.getoption("--full"):
        pytest.skip("--full option required to run this test")


@pytest.fixture(scope='session')
def http_url():
    return (
        'http://ovh.net/files/1Mio.dat',
        hashlib.sha1,
        '22c952ea2b497171d37b76f0830ef8d9911cfe9b',
        1048576,
    )


@pytest.fixture(scope='session')
def youtube_url():
    return (
        'https://www.youtube.com/watch?v=y8Kyi0WNg40',
        hashlib.sha1,
        '8f6e676fc6cfbec1408a55f0f6a25b62b5ade072',
        219662,
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
def test_urls(http_url, youtube_url, ftp_url, local_file_url):
    return [
        http_url,
        youtube_url,
        ftp_url,
        local_file_url,
    ]


@pytest.fixture(
    params=[
        ('http_url', multidl.downloaders.HttpDownloader),
        ('youtube_url', multidl.downloaders.YoutubeDownloader),
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
