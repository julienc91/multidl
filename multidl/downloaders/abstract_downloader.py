# -*- coding: utf-8 -*-

import os
import time
from abc import ABC, abstractmethod
from contextlib import suppress
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

    @staticmethod
    def can_handle_url(url):
        raise NotImplementedError

    @property
    def output(self):
        if self._output_file:
            return self._output_file

        base_file_name = self.get_file_name()
        if not base_file_name:
            raise RuntimeError('Cannot set output file for download')

        index = 0
        filename = base_file_name
        while index < 1000:
            filepath = os.path.join(self._output_directory, filename)
            if self.__try_create_output_file(filepath):
                return self.output

            index += 1
            filename, extension = os.path.splitext(base_file_name)
            filename = filename + "_" + str(index) + extension

        raise RuntimeError('Cannot set output file for download')

    def __try_create_output_file(self, filepath):
        try:
            with open(filepath, 'x'):
                self._output_file = filepath
        except FileExistsError:
            return None
        else:
            return self.output

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

    def _wait_in_state(self, state):
        while self.state == state:
            time.sleep(0.1)

    @abstractmethod
    def get_file_name(self):
        return ''

    @abstractmethod
    def start(self):
        if self.state != DownloadState.not_started:
            return

        with suppress(OSError):
            os.makedirs(os.path.dirname(self.output))
        self.state = DownloadState.started

    def _finish(self):
        if self.state == DownloadState.canceling:
            self.state = DownloadState.canceled
        elif self.state != DownloadState.error:
            self.state = DownloadState.finished

    def cancel(self):
        self.state = DownloadState.canceling
        self._wait_in_state(DownloadState.canceling)

    def delete_output(self):
        with suppress(OSError):
            os.remove(self.output)

    def pause(self):
        self.state = DownloadState.pausing
        self.state = DownloadState.paused

    def resume(self):
        self.state = DownloadState.resuming
        self.state = DownloadState.started

    @abstractmethod
    def get_progress(self):
        pass
