# -*- coding: utf-8 -*-

import os
import pytest

from multidl.constants import DownloadState
from multidl.downloaders.ftp_downloader import FtpDownloader


@pytest.mark.parametrize('url, expected', [
    ('ftp://example.com/dir/file1.txt', 'file1.txt'),
    ('ftp://user:password@example.com/dir/file2.txt', 'file2.txt'),
    ('ftp://user:password@example.com:2222/dir/file3.txt', 'file3.txt'),
])
def test_get_file_name(url, expected):
    downloader = FtpDownloader(url, '/tmp')
    assert downloader.get_file_name() == expected


def test_download(ftp_url, tempdir):
    url, hasher, expected_hash, expected_size = ftp_url
    downloader = FtpDownloader(url, tempdir)
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
