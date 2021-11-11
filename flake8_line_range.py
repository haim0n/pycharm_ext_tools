#!/usr/bin/env python

import os.path
import subprocess
import sys
from argparse import ArgumentParser


def validate_args(args):
    assert (args.start_line <= args.end_line), \
        f'Invalid line numbers: {args.start_line}..{args.end_line}'
    assert os.path.exists(args.filename), f'Non existing file: {args.filename}'
    assert os.path.exists(args.flake8_bin), f'Non existing file: {args.filename}'


def get_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('flake8_bin')
    arg_parser.add_argument('start_line', type=int)
    arg_parser.add_argument('end_line', type=int)
    arg_parser.add_argument('filename')

    args = arg_parser.parse_args()
    validate_args(args)

    return args


def _get_diff_header(start_line: int, end_line: int, filename: str) -> str:
    n_lines = end_line - start_line + 1
    return f"""+++ {filename}\t2021-10-21 15:22:42.023093147 +0000
@@ -{start_line},{n_lines} +{start_line},{n_lines} @@
    """


def run_flake8(flake8_bin, start_line, end_line, filename):
    header_lines = _get_diff_header(start_line, end_line, filename)
    try:
        subprocess.check_output(
            f'{flake8_bin} --diff -',
            input=header_lines.encode(),
            shell=True,
            close_fds=True,
        )
    except subprocess.CalledProcessError as e:
        output = e.output
        for line in output.decode().split('\n'):
            print(line)
        sys.exit(-1)


def main():
    args = get_args()
    run_flake8(args.flake8_bin,
               args.start_line,
               args.end_line,
               args.filename)


if __name__ == '__main__':
    main()
