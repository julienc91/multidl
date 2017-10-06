# -*- coding: utf-8 -*-

import os
import uuid
import logging
from queue import Queue, Empty
from threading import Thread

from multidl.downloaders import SCHEMES
from multidl.constants import DownloadState


class DownloadManager:

    def __init__(self, urls, output, nb_workers):
        self.output = output
        self.nb_workers = min(nb_workers, len(urls))
        self._urls = Queue()
        self._ongoing_downloads = Queue()
        self._state = DownloadState.not_started
        for url in urls:
            self._urls.put(url)

    @staticmethod
    def get_downloader(url):
        scheme = url.split('://')[0].lower()
        if scheme not in SCHEMES:
            raise NotImplementedError('No downloader for {} urls'
                                      .format(scheme))
        return SCHEMES[scheme]

    def process(self):
        for i in range(self.nb_workers):
            t = Thread(target=self.worker)
            t.start()

        self._urls.join()

    def worker(self):
        while True:
            try:
                url = self._urls.get_nowait()
            except Empty:
                break

            downloader = self.process_single_url(url, str(uuid.uuid4()))
            self._ongoing_downloads.put(downloader)
            downloader.start()
            self._urls.task_done()

    def process_single_url(self, url, download_identifier):
        try:
            downloader = self.get_downloader(url)
        except NotImplementedError as e:
            logging.error('{}: skipping {}'.format(e, url))
            return None

        output = os.path.join(self.output, download_identifier)
        download_process = downloader(url, output)
        return download_process

    def watcher(self):
        pass

    def pause(self):
        pass

    def cancel(self):
        pass
