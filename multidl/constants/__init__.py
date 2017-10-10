# -*- coding: utf-8 -*-

from enum import Enum


class DownloadState(Enum):
    not_started = 1
    started = 2
    paused = 3
    canceled = 4
    canceling = 5
    error = 6
    finished = 7


STATE_TRANSITIONS = {
    DownloadState.not_started: [DownloadState.started, DownloadState.paused,
                                DownloadState.canceling, DownloadState.error,
                                DownloadState.finished],
    DownloadState.started: [DownloadState.paused, DownloadState.canceling,
                            DownloadState.error, DownloadState.finished],
    DownloadState.paused: [DownloadState.started, DownloadState.canceling,
                           DownloadState.error, DownloadState.finished],
    DownloadState.canceling: [DownloadState.error, DownloadState.canceled,
                              DownloadState.finished],
    DownloadState.canceled: [DownloadState.error],
    DownloadState.error: [],
    DownloadState.finished: [],
}

STATE_NAMES = {
    DownloadState.not_started: 'not started',
    DownloadState.started: 'ongoing',
    DownloadState.paused: 'paused',
    DownloadState.canceling: 'canceling',
    DownloadState.canceled: 'canceled',
    DownloadState.error: 'error',
    DownloadState.finished: 'finished',
}