# -*- coding: utf-8 -*-

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
