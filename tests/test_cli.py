# -*- coding: utf-8 -*-

import pytest

from multidl.cli import parse_args


def test_parse_args(monkeypatch, config_file, tempdir):
    monkeypatch.setattr(
        'sys.argv',
        ['multidl',
         '-n', '4',
         '-c', config_file,
         '-o', tempdir])
    args = parse_args()

    assert args.n == 4
    assert args.config.name == config_file
    assert args.output_directory == tempdir


def test_parse_args_missing_parameters(monkeypatch, config_file, tempdir):
    args = [['multidl', '-n', '4', '-o', tempdir],
            ['multidl', '-n', '4', '-c', config_file]]

    for arg in args:
        monkeypatch.setattr('sys.argv', arg)
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_invalid_parameters(monkeypatch, config_file, tempdir):
    args = [['multidl', '-n', '0', '-c', config_file, '-o', tempdir],
            ['multidl', '-n', '-1', '-c', config_file, '-o', tempdir],
            ['multidl', '-n', 'a', '-c', config_file, '-o', tempdir],
            ['multidl', '-n', '4', '-c', 'foo', '-o', tempdir],
            ['multidl', '-n', '4', '-c', config_file, '-o', '/root'],
            ['multidl', '-n', '4', '-c', config_file, '-o', 'foo']]

    for arg in args:
        monkeypatch.setattr('sys.argv', arg)
        with pytest.raises(SystemExit):
            parse_args()
