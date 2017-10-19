# -*- coding: utf-8 -*-

import os

import pytest

import multidl.downloaders
from multidl.constants import DownloadState


@pytest.fixture(
    params=[
        ('http_url', multidl.downloaders.HttpDownloader),
        ('ftp_url', multidl.downloaders.FtpDownloader),
        ('local_file_url', multidl.downloaders.LocalFileDownloader),
    ]
)
def downloader(request):
    return request.getfixturevalue(request.param[0]), request.param[1]


def test_basic_download(downloader, tempdir):

    url, downloader = downloader
    url, hasher, expected_hash, expected_size = url

    downloader = downloader(url, tempdir)
    assert downloader.state == DownloadState.not_started

    downloader.start()
    assert downloader.state == DownloadState.finished
    downloaded_size, download_size = downloader.get_progress()

    assert downloaded_size == download_size
    assert downloaded_size == expected_size

    with open(downloader.output, 'rb') as f:
        content = f.read()

    os.remove(downloader.output)

    resulting_hash = hasher(content).hexdigest()
    assert resulting_hash == expected_hash


def test_cancel_download_before_start(downloader, tempdir):

    url, downloader = downloader
    url, hasher, expected_hash, expected_size = url

    downloader = downloader(url, tempdir)
    downloader.cancel()

    assert downloader.state == DownloadState.canceled

    downloaded_size, _ = downloader.get_progress()
    assert downloaded_size == 0
