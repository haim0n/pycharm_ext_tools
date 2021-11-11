#!/usr/bin/env python

"""Partial black formatter for PyCharm.

- To see partial black here:
 (https://blog.godatadriven.com/black-formatting-selection)

- This code is conversion of this shell script:
 (https://gist.github.com/BasPH/5e665273d5e4cb8a8eefb6f9d43b0b6d)
"""
import os
import sys
import tempfile

assert len(sys.argv) == 5, f'Invalid params: {sys.argv}'
black = sys.argv[1]
input_file = sys.argv[2]
start_line = int(sys.argv[3]) - 1
end_line = int(sys.argv[4])
black_args = '--skip-string-normalization'
# read input_file
with open(input_file, "rt", encoding="utf-8") as src_file:
    src_contents = [line for line in src_file]
    selection = src_contents[start_line:end_line]

print("Total file len: ", len(src_contents), "selected lines:", len(selection))

# it is a workaround for escaping windows os permission problem.
tmp_dir = tempfile.TemporaryDirectory()
tmp_file_name = os.path.join(tmp_dir.name, 'tmp_file_for_black')

# write selection on tmp_file
with open(tmp_file_name, "wt", encoding="utf-8") as f:
    f.writelines(selection)

# run black on tmp_file
cmd = f'{black} {black_args} {tmp_file_name}'
print("Run cmd:", cmd)
os.system(cmd)

# apply reformatted selection to original source file
with open(tmp_file_name, "rt", encoding="utf-8") as f:
    del src_contents[start_line:end_line]
    for i, line in enumerate(f):
        src_contents.insert(start_line + i, line)

# write to input_file
with open(input_file, "wt", encoding="utf-8") as f:
    f.writelines(src_contents)
