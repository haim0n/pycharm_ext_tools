# Pycharm External Tools
Support for formatting tools in Pycharm  
Currently supported are flake8 and black on a selected code block.

## Usage

### Flake8 [PEP8] validation on selected code block
![Flake8 on a selection](https://github.com/haim0n/pycharm_ext_tools/raw/master/resources/demo_flake8_line_range.gif)


### Black formatting on selected code block
![Flake8 on a selection](https://github.com/haim0n/pycharm_ext_tools/raw/master/resources/demo_black_line_range.gif)



### Installation

1. Install the repo (preferably in conda env or virtualenv):

`pip install git+https://github.com/haim0n/pycharm_ext_tools.git`

2. Add new external tool per utility (e.g. flake8) as follows:

`File -> Settings -> Tools -> External Tools -> '+' (Add)`

For conda environment named `dev` fill in the params:

```
Name:               Flake8 selection
Description:        Black formatter for selected lines
Program:            /home/haim0n/anaconda3/envs/dev/bin/python
Arguments:          -m pycharm_ext_tools.flake8_line_range /home/haim0n/anaconda3/envs/dev/bin/flake8 $SelectionStartLine$ $SelectionEndLine$ $FilePath$
Working Directory: $ProjectFileDir$
```

And you're done !