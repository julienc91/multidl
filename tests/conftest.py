# -*- coding: utf-8 -*-

import hashlib
import tempfile

import pytest


@pytest.fixture(scope='session')
def http_url():
    return (
        'http://ovh.net/files/1Mb.dat',
        hashlib.sha1,
        'a1684971de0de7327037f09fe0e1da3eeeae4115'
    )


@pytest.fixture(scope='session')
def tempdir():
    return tempfile.gettempdir()
