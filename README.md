# PDF Splitter

PDF Splitter is a script used to breakout defined regions of a PDF file into separate files.

## Prerequisites:

1. [Python 3+](https://www.python.org/downloads/)
2. [Ghostscript](https://www.ghostscript.com/doc/current) 
> Please ensure ghostscript has been setup correctly on your system and the command `gs` or `gswin64c` can be ran from a shell prompt shell.

## Using PDF Splitter

To use PDF Splitter `cd` into the directory with the `main.py` file and install dependencies using `pip3 install -r requirements.txt`.

To run the script, start by placing the file to be split into the `./input` folder, then run using `python ./main.py`, once complete the final files will be saved to the `./output` folder.

### Extra command line arguments:

`-s` Skip user confirmation

`-p` Display ongoing progress 

## Change Regions:

To change the regions to be split update the `REGIONS_TO_SPLIT` constant in the `main.py` file.

```py
"""
Each tuple is a pair of coordinates in this format:
[
  (lower_left_x, lower_left_y),
  (upper_right_x, upper_right_y)
]
"""
REGIONS_TO_SPLIT: List[List[Tuple[float, float]]] = [
    [
        (0, 420),
        (575, 750)
    ],
]
```


## Externally Used libraries:

- [PyPDF2](https://pypdf2.readthedocs.io/en/latest)
- [Ghostscript](https://www.ghostscript.com/doc/current)
