## signpdf
=======

A quick script to add signature images to PDFs, because I couldn't find
anything that worked well for the purpose under Linux.

Pros: should work with most PDFs, and with signatures as PNG's or JPG's.  It
preserves the incoming PDF's text format (e.g. doesn't convert every page to
images like some alternatives).   Just click a preview of the desired page to
indicate where your signature and date should go. 

Cons: hard coded signature file size

### Installation
------------

Install with pip:

    pip install signpdf

Or from git:

    git clone https://github.com/yourcelf/signpdf
    cd signpdf
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Usage
-----
```
signpdf.py [-h] [--date] [--output [OUTPUT]] [--pageno PAGENO] pdf [signature]

positional arguments:
  pdf                The pdf file to annotate
  signature          (optional - you can hardcode your sig file) The signature file (png, jpg)

optional arguments:
  -h, --help         show this help message and exit
  --date             enable clicking a second location for adding signature date.
  --output [OUTPUT]  Output file. Defaults to input filename plus '_signed'
  --pageno PAGENO    Which page to apply the signature (default= 1).
 ```
