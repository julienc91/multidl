# -*- coding: utf-8 -*-

from enum import Enum


class DownloadState(Enum):
    not_started = 1
    started = 2
    paused = 3
    canceled = 4
    error = 5
    finished = 6
