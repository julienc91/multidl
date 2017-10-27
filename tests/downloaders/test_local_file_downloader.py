# -*- coding: utf-8 -*-

import pytest

from multidl.downloaders.local_file_downloader import LocalFileDownloader


@pytest.mark.parametrize('url, expected', [
    ('file:///dir/file1.txt', 'file1.txt'),
    ('file:///file2.txt', 'file2.txt'),
])
def test_get_file_name(tmpdir, url, expected):
    downloader = LocalFileDownloader(url, str(tmpdir))
    assert downloader.get_file_name() == expected
