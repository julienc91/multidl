# -*- coding: utf-8 -*-

import pytest

from multidl.downloaders.http_downloader import HttpDownloader


@pytest.mark.parametrize('url, expected', [
    ('http://example.com/dir/file1.txt', 'file1.txt'),
    ('http://user:password@example.com/dir/file2.txt', 'file2.txt'),
    ('http://user:password@www.example.com:2222/dir/file3.txt', 'file3.txt'),
    ('https://www.example.com/dir/file4.txt', 'file4.txt'),
])
def test_get_file_name(tmpdir, url, expected):
    downloader = HttpDownloader(url, str(tmpdir))
    assert downloader.get_file_name() == expected
