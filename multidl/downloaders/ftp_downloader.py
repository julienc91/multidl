# -*- coding: utf-8 -*-

import os
from ftplib import FTP
from urllib.parse import urlparse

from multidl.downloaders.abstract_downloader import AbstractDownloader
from multidl.constants import DownloadState


class FtpDownloader(AbstractDownloader):

    def __init__(self, url, output, **options):
        super().__init__(url, output, **options)
        self._download_length = 0
        self._downloaded_length = 0
        self.__ftp = FTP()

    @staticmethod
    def can_handle_url(url):
        parsed_url = urlparse(url)
        return parsed_url.scheme == 'ftp'

    def __connect(self):

        parsed_url = urlparse(self.url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 0
        username = parsed_url.username
        password = parsed_url.password

        self.__ftp.connect(host=hostname, port=port)
        self.__ftp.login(username, password)

    def get_file_name(self):
        parsed_url = urlparse(self.url)
        return os.path.basename(parsed_url.path)

    def start(self):
        super().start()

        parsed_url = urlparse(self.url)
        path = parsed_url.path
        dirname = os.path.dirname(path)

        self.__connect()
        if dirname:
            self.__ftp.cwd(dirname)

        self._download_length = self.__ftp.size(path)
        remote_filename = os.path.basename(path)

        with open(self.output, 'wb') as f:
            self.__ftp.retrbinary("RETR " + remote_filename,
                                  lambda data: self.__write_chunk(f, data))
        self._finish()

    def __write_chunk(self, f, data):
        self._wait_in_state(DownloadState.paused)
        self._downloaded_length += len(data)
        f.write(data)

    def get_progress(self):
        return self._downloaded_length, self._download_length

    def cancel(self):
        super().cancel()
        if self.__ftp.sock:
            self.__ftp.abort()
        self.delete_output()
