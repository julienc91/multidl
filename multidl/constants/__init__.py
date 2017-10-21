# -*- coding: utf-8 -*-

from enum import Enum


class DownloadState(Enum):
    not_started = 1
    started = 2
    pausing = 3
    paused = 4
    resuming = 5
    canceling = 6
    canceled = 7
    error = 8
    finished = 9


STATE_TRANSITIONS = {
    DownloadState.not_started: [DownloadState.started, DownloadState.canceling,
                                DownloadState.error, DownloadState.finished],
    DownloadState.started: [DownloadState.pausing, DownloadState.canceling,
                            DownloadState.error, DownloadState.finished],
    DownloadState.pausing: [DownloadState.paused, DownloadState.error,
                            DownloadState.finished],
    DownloadState.paused: [DownloadState.resuming, DownloadState.canceling,
                           DownloadState.error, DownloadState.finished],
    DownloadState.resuming: [DownloadState.started, DownloadState.error,
                             DownloadState.finished],
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
