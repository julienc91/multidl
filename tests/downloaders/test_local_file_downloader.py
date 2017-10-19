# -*- coding: utf-8 -*-

import os

import pytest

from multidl.constants import DownloadState
from multidl.downloaders.local_file_downloader import LocalFileDownloader


@pytest.mark.parametrize('url, expected', [
    ('file:///dir/file1.txt', 'file1.txt'),
    ('file:///file2.txt', 'file2.txt'),
])
def test_get_file_name(url, expected):
    downloader = LocalFileDownloader(url, '/tmp')
    assert downloader.get_file_name() == expected


def test_download(local_file_url, tempdir):
    url, hasher, expected_hash, expected_size = local_file_url
    downloader = LocalFileDownloader(url, tempdir)
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
