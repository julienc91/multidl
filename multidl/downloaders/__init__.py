# -*- coding: utf-8 -*-

from multidl.downloaders.ftp_downloader import FtpDownloader
from multidl.downloaders.http_downloader import HttpDownloader

SCHEMES = {
    'ftp': FtpDownloader,
    'http': HttpDownloader,
    'https': HttpDownloader,
}
