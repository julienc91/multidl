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


@pytest.mark.parametrize('current_state, new_state', [
    (DownloadState.not_started, DownloadState.started),
    (DownloadState.not_started, DownloadState.canceling),
    (DownloadState.started, DownloadState.paused),
    (DownloadState.paused, DownloadState.started),
    (DownloadState.started, DownloadState.canceling),
    (DownloadState.started, DownloadState.finished),
])
def test_change_state(tempdir, current_state, new_state):

    download_manager = DownloadManager([], tempdir, 4)
    assert download_manager.state == DownloadState.not_started

    download_manager._state = current_state
    download_manager.state = new_state
    assert download_manager.state == new_state


@pytest.mark.parametrize('current_state, new_state', [
    (DownloadState.started, DownloadState.not_started),
    (DownloadState.started, DownloadState.started),
    (DownloadState.finished, DownloadState.paused),
    (DownloadState.canceling, DownloadState.started),
])
def test_change_state_invalid(tempdir, current_state, new_state):

    download_manager = DownloadManager([], tempdir, 4)
    assert download_manager.state == DownloadState.not_started

    download_manager._state = current_state
    with pytest.raises(TransitionError):
        download_manager.state = new_state
    assert download_manager.state == current_state
