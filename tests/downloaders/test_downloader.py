# -*- coding: utf-8 -*-

import os

import pytest

from multidl.constants import DownloadState
from multidl.exceptions import TransitionError


def test_download_multiple_files_same_name(downloader, tempdir):

    url, downloader = downloader
    url, _, _, _ = url

    downloaders = [
        downloader(url, tempdir)
        for _ in range(50)
    ]

    output_files = {
        downloader.output for downloader in downloaders
    }
    assert len(output_files) == len(downloaders)


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


def test_cancel_before_start(downloader, tempdir):

    url, downloader = downloader
    url, hasher, expected_hash, expected_size = url

    downloader = downloader(url, tempdir)
    downloader.cancel()

    assert downloader.state == DownloadState.canceled

    downloaded_size, _ = downloader.get_progress()
    assert downloaded_size == 0


def test_pause_before_start(downloader, tempdir):

    url, downloader = downloader
    url, hasher, expected_hash, expected_size = url

    downloader = downloader(url, tempdir)
    with pytest.raises(TransitionError):
        downloader.pause()

    assert downloader.state == DownloadState.not_started


def test_resume_before_start(downloader, tempdir):

    url, downloader = downloader
    url, hasher, expected_hash, expected_size = url

    downloader = downloader(url, tempdir)
    with pytest.raises(TransitionError):
        downloader.resume()

    assert downloader.state == DownloadState.not_started


def test_pause_after_start(downloader, tempdir):
    url, downloader = downloader
    url, hasher, expected_hash, expected_size = url

    downloader = downloader(url, tempdir)
    downloader._state = DownloadState.started

    downloader.pause()
    assert downloader.state == DownloadState.paused


def test_resume_after_pause(downloader, tempdir):
    url, downloader = downloader
    url, hasher, expected_hash, expected_size = url

    downloader = downloader(url, tempdir)
    downloader._state = DownloadState.paused

    downloader.resume()
    assert downloader.state == DownloadState.started
