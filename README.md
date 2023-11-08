## signpdf
### This fork:
Several improvements: 

    1) Direct clicking of PDF images
    
    2) Specify page number to sign on multi-page PDFs
    
    3) Add today's date to a second clicked location
    
    4) Add some text to the clicked location instead of signature (example: printed full name)

    5) Supports as many signatures or text adds as you want without restarting on a renamed file
    
    5) Rename output file ... `_signed_XX.pdf`  where `XX` are your initials
    
    6) Save your sig file location and your initials in a config file in your home dir. 



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
signpdf.py [-h] [--date] [--output [OUTPUT]] [--text] [--pageno PAGENO] pdf [signature]

positional arguments:
  pdf                The pdf file to annotate
  signature          (optional - you can hardcode your sig file) The signature file (png, jpg)

optional arguments:
  -h, --help         show this help message and exit
  --date             enable clicking a second location for adding signature date.
  --output [OUTPUT]  Output file. Defaults to input filename plus '_signed'
  --text             Instead of signature, you will be propted for text to insert
  --pageno PAGENO    Which page to apply the signature (default= 1).
 ```
