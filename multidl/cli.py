# -*- coding: utf-8 -*-

import os
import sys
import argparse

from multidl.download_manager import DownloadManager


def positive_integer(value):
    try:
        value = int(value)
        if value <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("{} is not a positive integer"
                                         .format(value))
    return value


def readable_directory(value):
    try:
        if (not os.path.isdir(value) or
                not os.access(value, os.R_OK)):
            raise ValueError
    except (ValueError, OSError):
        raise argparse.ArgumentTypeError("{} is not a valid directory"
                                         .format(value))
    return value


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='A file listing the targetted urls, '
                             'one item per line. Leave empty to read '
                             'from stdin.')
    parser.add_argument('-o', '--output-directory', required=True,
                        type=readable_directory,
                        help='Output directory.')
    parser.add_argument('-n', default=4, type=positive_integer,
                        help='Number of parallel downloads. Default is 4.')
    args = parser.parse_args()
    return args


def main():

    args = parse_args()

    urls = [url.strip() for url in args.config.readlines()]
    output_directory = args.output_directory
    nb_workers = args.n

    download_manager = DownloadManager(urls, output_directory, nb_workers)
    download_manager.process()
