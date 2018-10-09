# -*- coding: utf-8 -*-

from io import StringIO

import pytest

from multidl.cli import parse_args, main


def test_parse_args(monkeypatch, config_file, tmpdir):
    monkeypatch.setattr(
        'sys.argv',
        ['multidl',
         '-n', '4',
         '-c', config_file,
         '-o', str(tmpdir)])
    args = parse_args()

    assert args.n == 4
    assert args.config.name == config_file
    assert args.output_directory == str(tmpdir)


def test_parse_args_missing_parameters(monkeypatch, config_file):
    args = [['multidl', '-n', '4'],
            ['multidl', '-n', '4', '-c', config_file]]

    for arg in args:
        monkeypatch.setattr('sys.argv', arg)
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_invalid_parameters(monkeypatch, config_file, tmpdir):
    args = [['multidl', '-n', '0', '-c', config_file, '-o', str(tmpdir)],
            ['multidl', '-n', '-1', '-c', config_file, '-o', str(tmpdir)],
            ['multidl', '-n', 'a', '-c', config_file, '-o', str(tmpdir)],
            ['multidl', '-n', '4', '-c', 'foo', '-o', str(tmpdir)],
            ['multidl', '-n', '4', '-c', config_file, '-o', '/root'],
            ['multidl', '-n', '4', '-c', config_file, '-o', 'foo']]

    for arg in args:
        monkeypatch.setattr('sys.argv', arg)
        with pytest.raises(SystemExit):
            parse_args()


@pytest.mark.full
def test_run_from_cli_with_file(monkeypatch, config_file, tmpdir):
    monkeypatch.setattr('sys.argv', ['multidl', '-n', '4', '-c',
                                     config_file, '-o', str(tmpdir)])
    main()


@pytest.mark.full
def test_run_from_cli_with_stdin(monkeypatch, config_file, tmpdir):
    with open(config_file) as f:
        stdin = StringIO(f.read())

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.argv', ['multidl', '-n', '4', '-o', str(tmpdir)])
    main()
