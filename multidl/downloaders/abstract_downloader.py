# -*- coding: utf-8 -*-

import os
import time
from abc import ABC, abstractmethod
from threading import Lock

from multidl.constants import DownloadState, STATE_TRANSITIONS
from multidl.exceptions import TransitionError


class AbstractDownloader(ABC):

    def __init__(self, url, output_directory, **options):
        self.url = url
        self.options = options
        self._output_file = None
        self._output_directory = output_directory
        self._state = DownloadState.not_started
        self._error = None
        self._lock = Lock()

    @property
    def output(self):
        if self._output_file:
            return self._output_file

        base_file_name = self.get_file_name()
        if not base_file_name:
            raise RuntimeError('Cannot set output file for download')

        index = 0
        while index < 1000:
            if index == 0:
                filename = base_file_name
            else:
                filename, extension = os.path.splitext(base_file_name)
                filename = filename + "_" + str(index) + extension
            filepath = os.path.join(self._output_directory, filename)
            try:
                with open(filepath, 'x'):
                    self._output_file = filepath
            except FileExistsError:
                index += 1
            else:
                return self.output
        raise RuntimeError('Cannot set output file for download')

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        with self._lock:
            if value not in STATE_TRANSITIONS[self._state]:
                raise TransitionError(self._state, value)

            # if the download has not started yet, cancellation is immediate
            if value == DownloadState.canceling:
                if self._state == DownloadState.not_started:
                    value = DownloadState.canceled
            self._state = value

    @abstractmethod
    def get_file_name(self):
        return ''

    @abstractmethod
    def start(self):
        if self.state != DownloadState.not_started:
            return

        try:
            os.makedirs(os.path.dirname(self.output))
        except OSError:
            pass
        self.state = DownloadState.started

    def cancel(self):
        self.state = DownloadState.canceling
        while self.state == DownloadState.canceling:
            time.sleep(0.1)

    def pause(self):
        self.state = DownloadState.pausing
        self.state = DownloadState.paused

    def resume(self):
        self.state = DownloadState.resuming
        self.state = DownloadState.started

    @abstractmethod
    def get_progress(self):
        pass
