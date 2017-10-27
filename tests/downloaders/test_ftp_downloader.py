# -*- coding: utf-8 -*-

import pytest

from multidl.downloaders.ftp_downloader import FtpDownloader


@pytest.mark.parametrize('url, expected', [
    ('ftp://example.com/dir/file1.txt', 'file1.txt'),
    ('ftp://user:password@example.com/dir/file2.txt', 'file2.txt'),
    ('ftp://user:password@example.com:2222/dir/file3.txt', 'file3.txt'),
])
def test_get_file_name(tmpdir, url, expected):
    downloader = FtpDownloader(url, str(tmpdir))
    assert downloader.get_file_name() == expected
