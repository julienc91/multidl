# -*- coding: utf-8 -*-

from multidl.downloaders.http_downloader import HttpDownloader

SCHEMES = {
    'http': HttpDownloader,
    'https': HttpDownloader,
}
