#!/usr/bin/env python

import os
import time
import argparse
import tempfile
import PyPDF2
import datetime
from reportlab.pdfgen import canvas

parser = argparse.ArgumentParser("Add signatures to PDF files")
parser.add_argument("pdf", help="The pdf file to annotate")
parser.add_argument("signature", help="The signature file (png, jpg)")
parser.add_argument("--date", action='store_true')
parser.add_argument("--output", nargs='?',
        help="Output file. Defaults to input filename plus '_signed'")
parser.add_argument("--coords", nargs='?', default='2x100x100x125x40',
        help="Coordinates to place signature. Format: PAGExXxYxWIDTHxHEIGHT.  1x200x300x125x40 means page 1, 200 units horizontally from the bottom left, 300 units vertically from the bottom left, 125 units wide, 40 units tall. Pages count starts at 1 (1-based indexing).  Units are pdf-standard units (1/72 inch).")

def _get_tmp_filename(suffix=".pdf"):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        return fh.name

def sign_pdf(args):
    #TODO: use a gui or something.... for now, just trial-and-error the coords
    page_num, x1, y1, width, height = [int(a) for a in args.coords.split("x")]
    page_num -= 1

    output_filename = args.output or "{}_signed{}".format(
        *os.path.splitext(args.pdf)
    )

    pdf_fh = open(args.pdf, 'rb')
    sig_tmp_fh = None

    pdf = PyPDF2.PdfFileReader(pdf_fh)
    writer = PyPDF2.PdfFileWriter()
    sig_tmp_filename = None

    for i in range(0, pdf.getNumPages()):
        page = pdf.getPage(i)

        if i == page_num:
            # Create PDF for signature
            sig_tmp_filename = _get_tmp_filename()
            c = canvas.Canvas(sig_tmp_filename, pagesize=page.cropBox)
            c.drawImage(args.signature, x1, y1, width, height)
            if args.date:
                c.drawString(x1 + width, y1, datetime.datetime.now().strftime("%Y-%m-%d"))
            c.showPage()
            c.save()

            # Merge PDF in to original page
            sig_tmp_fh = open(sig_tmp_filename, 'rb')
            sig_tmp_pdf = PyPDF2.PdfFileReader(sig_tmp_fh)
            sig_page = sig_tmp_pdf.getPage(0)
            sig_page.mediaBox = page.mediaBox
            page.mergePage(sig_page)

        writer.addPage(page)

    with open(output_filename, 'w') as fh:
        writer.write(fh)

    for handle in [pdf_fh, sig_tmp_fh]:
        if handle:
            handle.close()
    if sig_tmp_filename:
        os.remove(sig_tmp_filename)

def main():
    sign_pdf(parser.parse_args())

if __name__ == "__main__":
    main()
