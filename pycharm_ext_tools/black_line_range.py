#!/usr/bin/env python

"""Partial black formatter for PyCharm."""
import os
import subprocess
import tempfile
from argparse import ArgumentParser


def run_black(black_bin, start_line, end_line, input_file):
    black_args = '--skip-string-normalization --line-length=120'

    with open(input_file, "rt", encoding="utf-8") as src_file:
        src_contents = [line for line in src_file]
        selection = src_contents[start_line:end_line]

    print("Total file len: ", len(src_contents), "selected lines:",
          len(selection))

    # workaround escaping windows os permission
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_file_name = os.path.join(tmp_dir.name, 'tmp_file_for_black')

    # write selection to tmp_file
    with open(tmp_file_name, "wt", encoding="utf-8") as f:
        f.writelines(selection)

    # run black on tmp_file
    cmd = f'{black_bin} {black_args} {tmp_file_name}'
    for line in subprocess.getoutput(cmd).split('\n'):
        print(line)

    # apply reformatted selection to original source file
    with open(tmp_file_name, "rt", encoding="utf-8") as f:
        del src_contents[start_line:end_line]
        for i, line in enumerate(f):
            src_contents.insert(start_line + i, line)

    # write to input_file
    with open(input_file, "wt", encoding="utf-8") as f:
        f.writelines(src_contents)


def validate_args(args):
    assert (
            args.start_line <= args.end_line
    ), f'Invalid line range: {args.start_line}..{args.end_line}'


def get_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('black_bin')
    arg_parser.add_argument('start_line', type=int)
    arg_parser.add_argument('end_line', type=int)
    arg_parser.add_argument('filename')
    args = arg_parser.parse_args()
    args.start_line -= 1
    validate_args(args)

    return args


def main():
    args = get_args()
    run_black(args.black_bin, args.start_line, args.end_line, args.filename)


if __name__ == '__main__':
    main()
