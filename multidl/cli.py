# -*- coding: utf-8 -*-

import argparse

from multidl.download_manager import DownloadManager


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True,
                        type=argparse.FileType('r'),
                        help='A file listing the targetted urls, '
                             'one item per line.')
    parser.add_argument('-o', '--output-directory', required=True,
                        help='Output directory.')
    parser.add_argument('-n', default=10, type=int,
                        help='Number of parallel downloads')
    args = parser.parse_args()
    if args.n <= 0:
        raise argparse.ArgumentError('n', 'n must be strictly positive')
    return args


def main():

    args = parse_args()

    urls = [url.strip() for url in args.config.readlines()]
    output_directory = args.output_directory
    nb_workers = args.n

    download_manager = DownloadManager(urls, output_directory, nb_workers)
    download_manager.process()
