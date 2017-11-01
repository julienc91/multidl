# -*- coding: utf-8 -*-

import os
import time
from queue import Queue, Empty
from threading import Thread
from urllib.parse import urlparse

from tqdm import tqdm

from multidl.constants import DownloadState, STATE_TRANSITIONS
from multidl.downloaders import SCHEMES
from multidl.exceptions import TransitionError


class DownloadManager:

    def __init__(self, urls, output_directory, nb_workers, **options):

        self.output_directory = output_directory
        self.nb_workers = min(nb_workers, len(urls))
        self.options = options

        self._urls = Queue()
        self._state = DownloadState.not_started
        self._download_handlers = []

        # initialize the queue
        for i, url in enumerate(urls):
            self._urls.put((i, url))
            self._download_handlers.append(DownloadHandler(url))

    def log(self, *args, **kwargs):
        if self.options.get('quiet'):
            return
        print(*args, **kwargs)

    @staticmethod
    def get_downloader(url):

        parsed_url = urlparse(url)
        for downloader in SCHEMES.get(parsed_url.scheme, []):
            if downloader.can_handle_url(url):
                return downloader

        raise NotImplementedError('No downloader for {} urls'
                                  .format(parsed_url.scheme))

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        current_state = self._state
        if value not in STATE_TRANSITIONS[current_state]:
            raise TransitionError(current_state, value)
        self._state = value

    def process(self):
        self.state = DownloadState.started

        try:
            watcher = Thread(target=self.watcher)
            watcher.start()

            for _ in range(self.nb_workers):
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
                index, url = self._urls.get_nowait()
            except Empty:
                break

            downloader = self.process_single_url(url)
            if downloader:
                self._download_handlers[index].downloader = downloader
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

    def watcher(self):

        while True:

            for download_handler in self._download_handlers:
                download_handler.update_progress()

            if not self._urls.unfinished_tasks:
                break
            time.sleep(1)

        self.state = DownloadState.finished
        tqdm.write('')

    def pause(self):
        self.state = DownloadState.pausing
        for download_handler in self._download_handlers:
            download_handler.pause()
        self.state = DownloadState.paused

    def resume(self):
        self.state = DownloadState.resuming
        for download_handler in self._download_handlers:
            download_handler.resume()
        self.state = DownloadState.started

    def cancel(self):
        self.state = DownloadState.canceling
        for download_handler in self._download_handlers:
            download_handler.cancel()
        self.state = DownloadState.canceled


class DownloadHandler:

    def __init__(self, url):
        self.url = url
        self.downloader = None
        self.progress_bar = None

    def update_progress(self):
        if not self.downloader:
            return

        downloaded, total = self.downloader.get_progress()

        if self.progress_bar is None:
            bar_name = os.path.basename(self.downloader.output)
            self.progress_bar = tqdm(
                total=total, desc=bar_name, disable=False,
                unit='b', unit_scale=True, unit_divisor=1024)
        progress = downloaded - self.progress_bar.n
        self.progress_bar.update(progress)

        if self.downloader.state in [DownloadState.finished,
                                     DownloadState.canceled,
                                     DownloadState.error]:
            self.progress_bar.close()

    def pause(self):
        self.downloader and self.downloader.pause()

    def resume(self):
        self.downloader and self.downloader.resume()

    def cancel(self):
        self.downloader and self.downloader.cancel()
