# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from threading import Lock

from multidl.constants import DownloadState


class AbstractDownloader(ABC):

    def __init__(self, url, output, **options):
        self.url = url
        self.options = options
        self.output = output
        self._state = DownloadState.not_started
        self._lock = Lock()

    def get_state(self):
        return self._state

    @abstractmethod
    def start(self):
        with self._lock:
            if self._state != DownloadState.not_started:
                raise RuntimeError
            self._state = DownloadState.started

    def cancel(self):
        with self._lock:
            if self._state not in [DownloadState.started, DownloadState.paused,
                                   DownloadState.canceled, DownloadState.error]:
                raise RuntimeError
            self._state = DownloadState.canceled

    @abstractmethod
    def get_progress(self):
        with self._lock:
            if self._state not in [DownloadState.started, DownloadState.paused,
                                   DownloadState.canceled, DownloadState.error,
                                   DownloadState.finished]:
                raise RuntimeError

    def pause(self):
        with self._lock:
            if self._state != DownloadState.started:
                raise RuntimeError
            self._state = DownloadState.paused

    def resume(self):
        with self._lock:
            if self._state != DownloadState.paused:
                raise RuntimeError
            self._state = DownloadState.started