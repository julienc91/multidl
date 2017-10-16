# -*- coding: utf-8 -*-

import os
import time
from urllib.parse import urlparse

from multidl.downloaders.abstract_downloader import AbstractDownloader
from multidl.constants import DownloadState


class LocalFileDownloader(AbstractDownloader):

    CHUNK_SIZE = 1024 * 16

    def __init__(self, url, output, **options):
        super().__init__(url, output, **options)
        self._download_length = 0
        self._downloaded_length = 0

    def get_file_name(self):
        parsed_url = urlparse(self.url)
        return os.path.basename(parsed_url.path)

    def start(self):
        super().start()

        parsed_url = urlparse(self.url)
        path = parsed_url.path

        self._download_length = os.path.getsize(path)

        with open(self.output, 'wb') as fw, open(path, 'rb') as fr:
            while True:
                data = self.__get_chunk(fr)
                if not data:
                    break
                self._downloaded_length += len(data)
                fw.write(data)

        if self.state == DownloadState.canceling:
            self.state = DownloadState.canceled
        elif self.state != DownloadState.error:
            self.state = DownloadState.finished

    def __get_chunk(self, f):
        while self.state == DownloadState.paused:
            time.sleep(0.1)
        return f.read(self.CHUNK_SIZE)

    def get_progress(self):
        super().get_progress()
        return self._downloaded_length, self._download_length

    def cancel(self):
        super().cancel()
        try:
            os.remove(self.output)
        except OSError:
            pass
