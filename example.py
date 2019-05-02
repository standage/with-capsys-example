#!/usr/bin/env python3

import argparse
from gzip import open as gzopen
import json
import sys
from tempfile import NamedTemporaryFile


def myopen(filename, mode):
    if mode not in ('r', 'w'):
        raise ValueError('invalid mode "{}"'.format(mode))
    if filename in ['-', None]:
        filehandle = sys.stdin if mode == 'r' else sys.stdout
        return filehandle
    openfunc = open
    if filename.endswith('.gz'):
        openfunc = gzopen
        mode += 't'
    return openfunc(filename, mode)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', help='output file; default is terminal')
    parser.add_argument('data')
    return parser


def main(args):
    data = {
        'really_important_data': args.data,
        'some_more_data': 42,
        'on_a_roll_here': 3.14159,
    }
    with myopen(args.out, 'w') as fh:
        json.dump(data, fh, indent=4)


def test_output_file():
    with NamedTemporaryFile(suffix='.json.gz') as outfile:
        arglist = ['--out', outfile.name, 'SuperSecretData']
        args = cli().parse_args(arglist)
        main(args)
        with myopen(outfile.name, 'r') as fh:
            data = json.load(fh)
    assert data['really_important_data'] == 'SuperSecretData'


def test_output_terminal(capsys):
    arglist = ['SuperSecretData']
    args = cli().parse_args(arglist)
    main(args)
    out, err = capsys.readouterr()
    assert '"really_important_data": "SuperSecretData"' in out


if __name__ == '__main__':
    args = cli().parse_args()
    main(args)
