# -*- coding: utf-8 -*-

import pytest

from multidl.constants import DownloadState
from multidl.exceptions import TransitionError
from multidl.download_manager import DownloadManager


def test_get_downloader(downloader):
    url, downloader = downloader
    url, _, _, _ = url

    res = DownloadManager.get_downloader(url)
    assert res == downloader


def test_get_downloader_invalid_url():
    with pytest.raises(NotImplementedError):
        DownloadManager.get_downloader('foo://bar')


@pytest.mark.parametrize('current_state, new_state', [
    (DownloadState.not_started, DownloadState.started),
    (DownloadState.not_started, DownloadState.canceling),
    (DownloadState.started, DownloadState.pausing),
    (DownloadState.pausing, DownloadState.paused),
    (DownloadState.paused, DownloadState.resuming),
    (DownloadState.resuming, DownloadState.started),
    (DownloadState.started, DownloadState.canceling),
    (DownloadState.canceling, DownloadState.canceled),
    (DownloadState.started, DownloadState.finished),
])
def test_change_state(tmpdir, current_state, new_state):

    download_manager = DownloadManager([], str(tmpdir), 4)
    assert download_manager.state == DownloadState.not_started

    download_manager._state = current_state
    download_manager.state = new_state
    assert download_manager.state == new_state


@pytest.mark.parametrize('current_state, new_state', [
    (DownloadState.started, DownloadState.not_started),
    (DownloadState.not_started, DownloadState.paused),
    (DownloadState.started, DownloadState.started),
    (DownloadState.started, DownloadState.resuming),
    (DownloadState.finished, DownloadState.paused),
    (DownloadState.canceling, DownloadState.started),
])
def test_change_state_invalid(tmpdir, current_state, new_state):

    download_manager = DownloadManager([], str(tmpdir), 4)
    assert download_manager.state == DownloadState.not_started

    download_manager._state = current_state
    with pytest.raises(TransitionError):
        download_manager.state = new_state
    assert download_manager.state == current_state


@pytest.mark.full
def test_basic_downloads(test_urls, tmpdir):

    urls = [url[0] for url in test_urls]

    download_manager = DownloadManager(urls, str(tmpdir), 4)
    assert download_manager.state == DownloadState.not_started
    download_manager.process()

    assert download_manager.state == DownloadState.finished


@pytest.mark.full
def test_cancel_before_start(test_urls, tmpdir):

    urls = [url[0] for url in test_urls]

    download_manager = DownloadManager(urls, str(tmpdir), 4)
    download_manager.cancel()
    assert download_manager.state == DownloadState.canceled


@pytest.mark.full
def test_basic_download_invalid_url(tmpdir):

    urls = ['foo://bar']
    download_manager = DownloadManager(urls, str(tmpdir), 4)
    download_manager.process()

    assert download_manager.state == DownloadState.finished
