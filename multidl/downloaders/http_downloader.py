# -*- coding: utf-8 -*-

import os
from contextlib import suppress
from urllib.parse import urlparse

import requests

from multidl.downloaders.abstract_downloader import AbstractDownloader
from multidl.constants import DownloadState


class HttpDownloader(AbstractDownloader):

    def __init__(self, url, output, **options):
        super().__init__(url, output, **options)
        self._download_length = 0
        self._downloaded_length = 0
        self.__request = None

    @staticmethod
    def can_handle_url(url):
        parsed_url = urlparse(url)
        return parsed_url.scheme in ['http', 'https']

    def get_file_name(self):
        parsed_url = urlparse(self.url)
        return os.path.basename(parsed_url.path) or 'index.html'

    def start(self):
        super().start()

        self.__request = requests.get(self.url, stream=True)
        with suppress(KeyError, ValueError):
            self._download_length = int(self.__request
                                        .headers['content-length'])

        with open(self.output, "wb") as f:
            for chunk in self.__get_chunk():
                f.write(chunk)
                self._downloaded_length += len(chunk)
        self._finish()

    def __get_chunk(self):
        for chunk in self.__request.iter_content(chunk_size=1024):
            self._wait_in_state(DownloadState.paused)
            state = self.state

            if state == DownloadState.started and chunk:
                # ignore keep-alive chunks
                yield chunk
            elif state != DownloadState.started:
                break

    def get_progress(self):
        return self._downloaded_length, self._download_length

    def cancel(self):
        super().cancel()
        self.delete_output()
