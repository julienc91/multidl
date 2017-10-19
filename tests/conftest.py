# -*- coding: utf-8 -*-

import os
import uuid
import hashlib
import tempfile

import pytest


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
        os.path.abspath(filename),
        hashlib.sha1,
        content_hash,
        len(content),
    )

    os.remove(filename)


@pytest.fixture(scope='session')
def tempdir():
    return tempfile.gettempdir()
