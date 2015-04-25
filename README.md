signpdf
=======

A quick script to add signature images to PDFs, because I couldn't find
anything that worked well for the purpose under Linux.

Pros: should work with most PDFs, and with signatures as PNG's or JPG's.  It
preserves the incoming PDF's text format (e.g. doesn't convert every page to
images like some alternatives).

Cons: no gui yet.

Installation
------------

Install with pip:

    pip install signpdf

Or from git:

    git clone https://github.com/yourcelf/signpdf
    cd signpdf
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Usage
-----

Sign the first page of "contract.pdf" with the signature "sig.png":

    signpdf contract.pdf sig.png --coords 1x100x100x150x40

Coordinates format is:  ``<pagenum>x<x-coord>x<y-coord>x<width>x<height>``.
 - ``<pagenum>`` the page number, count starts at 1.
 - ``<x-coord>`` horizontal distance from bottom-left corner in PDF units (1/72 inch).
 - ``<y-coord>`` vertical distance from bottom-left corner in PDF units (1/72 inch).
 - ``<width>`` width of signature in PDF units (1/72 inch).
 - ``<height>`` height of signature in PDF units (1/72 inch)

Other options:

 - ``--date`` Append a date to the right of the signature.
 - ``--output`` Destination filename.  Default is to append ``_signed`` to the incoming PDF name.

For more usage details, run ``signpdf --help``.
