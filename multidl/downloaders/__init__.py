# -*- coding: utf-8 -*-

from multidl.downloaders.local_file_downloader import LocalFileDownloader
from multidl.downloaders.ftp_downloader import FtpDownloader
from multidl.downloaders.http_downloader import HttpDownloader

SCHEMES = {
    'file': [LocalFileDownloader],
    'ftp': [FtpDownloader],
    'http': [HttpDownloader],
    'https': [HttpDownloader],
}

try:
    from multidl.downloaders.youtube_downloader import YoutubeDownloader
    SCHEMES['http'].insert(0, YoutubeDownloader)
    SCHEMES['https'].insert(0, YoutubeDownloader)
except ImportError:
    pass
