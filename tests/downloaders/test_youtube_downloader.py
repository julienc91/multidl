# -*- coding: utf-8 -*-

import pytest

from multidl.downloaders.youtube_downloader import YoutubeDownloader


@pytest.mark.full
@pytest.mark.parametrize('url, expected', [
    ('https://www.youtube.com/watch?v=y8Kyi0WNg40', 'Dramatic Look.webm'),
])
def test_get_file_name(tmpdir, url, expected):
    downloader = YoutubeDownloader(url, str(tmpdir))
    assert downloader.get_file_name() == expected
