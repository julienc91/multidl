# -*- coding: utf-8 -*-

import re
import os

import pytube

from multidl.downloaders.abstract_downloader import AbstractDownloader
from multidl.constants import DownloadState


class YoutubeDownloader(AbstractDownloader):

    CHUNK_SIZE = 1024 * 16

    def __init__(self, url, output, **options):
        super().__init__(url, output, **options)
        self._download_length = 0
        self._downloaded_length = 0
        self.yt = pytube.YouTube(self.url)
        self.stream = self.yt.streams.first()

    @staticmethod
    def can_handle_url(url):
        return re.match(r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+', url)

    def get_file_name(self):
        return self.stream.default_filename

    def start(self):
        super().start()

        self.yt.register_on_progress_callback(
            lambda *args: self.__get_chunk(*args))
        self._download_length = self.stream.filesize

        self.stream.download(os.path.dirname(self.output))
        self._finish()

    def __get_chunk(self, *args):
        _, chunk, _, bytes_remaining = args
        self._wait_in_state(DownloadState.paused)
        self._downloaded_length += len(chunk)
        self._download_length = self._downloaded_length + bytes_remaining

    def get_progress(self):
        return self._downloaded_length, self._download_length

    def cancel(self):
        super().cancel()
        self.delete_output()
