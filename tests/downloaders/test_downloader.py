# -*- coding: utf-8 -*-

import os

import pytest

from multidl.constants import DownloadState
from multidl.exceptions import TransitionError


@pytest.mark.full
def test_download_multiple_files_same_name(downloader, tmpdir):

    url, downloader = downloader
    url, _, _, _ = url

    downloaders = [
        downloader(url, str(tmpdir))
        for _ in range(50)
    ]

    output_files = {
        downloader.output for downloader in downloaders
    }
    assert len(output_files) == len(downloaders)


@pytest.mark.full
def test_basic_download(downloader, tmpdir):

    url, downloader = downloader
    url, hasher, expected_hash, expected_size = url

    downloader = downloader(url, str(tmpdir))
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


@pytest.mark.full
def test_cancel_before_start(downloader, tmpdir):

    url, downloader = downloader
    url, _, _, _ = url

    downloader = downloader(url, str(tmpdir))
    downloader.cancel()

    assert downloader.state == DownloadState.canceled

    downloaded_size, _ = downloader.get_progress()
    assert downloaded_size == 0


@pytest.mark.full
def test_pause_before_start(downloader, tmpdir):

    url, downloader = downloader
    url, _, _, _ = url

    downloader = downloader(url, str(tmpdir))
    with pytest.raises(TransitionError):
        downloader.pause()

    assert downloader.state == DownloadState.not_started


@pytest.mark.full
def test_resume_before_start(downloader, tmpdir):

    url, downloader = downloader
    url, _, _, _ = url

    downloader = downloader(url, str(tmpdir))
    with pytest.raises(TransitionError):
        downloader.resume()

    assert downloader.state == DownloadState.not_started


@pytest.mark.full
def test_pause_after_start(downloader, tmpdir):
    url, downloader = downloader
    url, _, _, _ = url

    downloader = downloader(url, str(tmpdir))
    downloader._state = DownloadState.started

    downloader.pause()
    assert downloader.state == DownloadState.paused


@pytest.mark.full
def test_resume_after_pause(downloader, tmpdir):
    url, downloader = downloader
    url, _, _, _ = url

    downloader = downloader(url, str(tmpdir))
    downloader._state = DownloadState.paused

    downloader.resume()
    assert downloader.state == DownloadState.started


def test_can_handle_url(downloader):
    url, downloader = downloader
    url, _, _, _ = url

    assert downloader.can_handle_url(url)
