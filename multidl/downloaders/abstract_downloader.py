# -*- coding: utf-8 -*-

import time
from abc import ABC, abstractmethod
from threading import Lock

from multidl.constants import DownloadState, STATE_TRANSITIONS
from multidl.exceptions import TransitionError


class AbstractDownloader(ABC):

    def __init__(self, url, output, **options):
        self.url = url
        self.options = options
        self.output = output
        self._state = DownloadState.not_started
        self._error = None
        self._lock = Lock()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        with self._lock:
            if value not in STATE_TRANSITIONS[self._state]:
                raise TransitionError(self._state, value)
            self._state = value

    @abstractmethod
    def start(self):
        self.state = DownloadState.started

    def cancel(self):
        self.state = DownloadState.canceling
        while self.state == DownloadState.canceling:
            time.sleep(0.1)

    def pause(self):
        self.state = DownloadState.paused

    def resume(self):
        self.state = DownloadState.started

    @abstractmethod
    def get_progress(self):
        pass
