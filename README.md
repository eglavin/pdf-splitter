# Payslipper by eglavin

Payslipper is a program used to breakout regions in a single PDF file into multiple PDF files.

## Prerequisites:

> Please ensure ghostscript has been setup correctly on your system and the command `gs` or `gswin64c` can be ran from the Terminal / Powershell respectively.

## Using Payslipper


To use Payslipper `cd` into the directory with the main file and run it using the following command:

```ps1
python ./main.py
```

### Extra command line arguments:

`-s` Skip user confirmation

`-p` Display ongoing progress 


## Externally Used libraries:

- [PyPDF2](https://pypdf2.readthedocs.io/en/latest)
- [Ghostscript](https://www.ghostscript.com/doc/current)
