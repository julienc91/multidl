# -*- coding: utf-8 -*-

import os
import time
from queue import Queue, Empty
from threading import Thread

from multidl.constants import DownloadState, STATE_TRANSITIONS, STATE_NAMES
from multidl.downloaders import SCHEMES
from multidl.exceptions import TransitionError


class DownloadManager:

    def __init__(self, urls, output_directory, nb_workers, **options):

        self.output_directory = output_directory
        self.nb_workers = min(nb_workers, len(urls))
        self.options = options

        self._urls = Queue()
        self._ongoing_downloads = Queue()
        self._finished_downloads = []
        self._state = DownloadState.not_started

        # initialize the queue
        for url in urls:
            self._urls.put(url)

    def log(self, *args, **kwargs):
        if self.options.get('quiet'):
            return
        print(*args, **kwargs)

    @staticmethod
    def get_downloader(url):
        scheme = url.split('://')[0].lower()
        if scheme not in SCHEMES:
            raise NotImplementedError('No downloader for {} urls'
                                      .format(scheme))
        return SCHEMES[scheme]

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        current_state = self._state
        if value not in STATE_TRANSITIONS[current_state]:
            raise TransitionError(current_state, value)
        self._state = value

    def _downloaders(self):
        """
        Helper function to iterate over self._ongoing_downloads once, and then
        put back every element into the queue.
        :return: iterator of downloaders
        """
        downloaders = []
        while True:
            try:
                downloader = self._ongoing_downloads.get_nowait()
            except Empty:
                break

            yield downloader
            downloaders.append(downloader)

        for downloader in downloaders:
            self._ongoing_downloads.put(downloader)

    def process(self):
        self.state = DownloadState.started

        try:
            watcher = Thread(target=self.watcher)
            watcher.start()

            for i in range(self.nb_workers):
                t = Thread(target=self.worker)
                t.start()

            self._urls.join()
            watcher.join()
        except KeyboardInterrupt:
            self.cancel()

    def worker(self):
        while True:
            state = self.state
            if state not in [DownloadState.paused, DownloadState.started]:
                break

            if state == DownloadState.paused:
                time.sleep(0.1)
                continue

            try:
                url = self._urls.get_nowait()
            except Empty:
                break

            downloader = self.process_single_url(url)
            if downloader:
                self._ongoing_downloads.put(downloader)
                downloader.start()
            self._urls.task_done()

    def process_single_url(self, url):
        try:
            downloader = self.get_downloader(url)
        except NotImplementedError as e:
            self.log('{}: skipping {}'.format(e, url))
            return None

        output = os.path.join(self.output_directory)
        download_process = downloader(url, output)
        return download_process

    def _print_downloader_state(self, downloader):
        state = downloader.state
        if state in [DownloadState.finished, DownloadState.canceled, DownloadState.error]:
            self.log('{}: {}'.format(downloader.url, STATE_NAMES[state]))
        else:
            if state == DownloadState.started:
                downloaded, total = downloader.get_progress()
                self.log('{}: {} / {}'.format(downloader.url, downloaded, total))

    def watcher(self):
        while (self._urls.unfinished_tasks or
               not self._ongoing_downloads.empty()):

            for downloader in self._finished_downloads:
                self._print_downloader_state(downloader)

            downloaders = []
            while True:
                try:
                    downloader = self._ongoing_downloads.get_nowait()
                except Empty:
                    break
                else:
                    downloader_state = downloader.state
                    self._print_downloader_state(downloader)
                    if downloader_state in [DownloadState.finished,
                                            DownloadState.canceled,
                                            DownloadState.error]:
                        self._finished_downloads.append(downloader)
                    else:
                        downloaders.append(downloader)

            for downloader in downloaders:
                self._ongoing_downloads.put(downloader)

            self.log('----------------------')
            time.sleep(1)
        self.state = DownloadState.finished

    def pause(self):
        self.state = DownloadState.pausing
        for downloader in self._downloaders():
            downloader.pause()
        self.state = DownloadState.paused

    def resume(self):
        self.state = DownloadState.resuming
        for downloader in self._downloaders():
            downloader.resume()
        self.state = DownloadState.started

    def cancel(self):
        self.state = DownloadState.canceling
        for downloader in self._downloaders():
            downloader.cancel()
        self.state = DownloadState.canceled
