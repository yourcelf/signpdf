#!/usr/bin/python3

import os
import time
import argparse
import tempfile
import PyPDF2
import datetime
from reportlab.pdfgen import canvas
# future: to support decrypting sigature file
#from PIL import Image


# for gui clicking
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

import time
 
YOUR_FAV_SIGNATURE_IMAGE = '/home/blake/xxxxxxxxxxxx'

parser = argparse.ArgumentParser(">signpdf.py")
# future - store encrypted signature image
#parser.add_argument('key', help='key to decript your signature file')
parser.add_argument("pdf", help="The pdf file to annotate")
# signature is now optional- a default is available
parser.add_argument("signature", nargs='?', 
        help="(optional)The signature file (png, jpg)")
parser.add_argument("--date", action='store_true',
        help='enable clicking a second location for adding signature date.')
parser.add_argument("--output", nargs='?',
        help="Output file. Defaults to input filename plus '_signed'")
parser.add_argument("--pageno", help="Which page to apply the signature (default= 1).")

def tellme(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()
    
    
    
screenscale = 1.5   # matplotlib display inches over paper size inches 
positscale  = 1.0
pdfdpi = 72.0       # PDF dots per inch

def co_xform(p1):   # assumes paper = US Letter
    pageheightIn = 11.0
    xfudge = 0
    yfudge = 0
    x1 = p1[0] + xfudge
    y1 = p1[1] + yfudge
    x2 = int((0.5+x1)*positscale)
    y2 = int((0.5+ pageheightIn*pdfdpi - y1)*positscale)
    return [x2,y2]
    
def sigbox(filename):
    # compute signature size in pixels
    #  TODO: open the signature file and figure out its height & width
    #    (but do we know the dpi??)
    sx = 2.0  # in    ###   hard coded for now
    sy = 0.625 # in
    x = int(0.5+pdfdpi*sx)
    y = int(0.5+pdfdpi*sy)
    return [x,y]
    
def sig_descender_offset():  # vertical shift to allow descenders below click pt
    # 
    #  future: figure this value out by image analysis of signature!!
    #
    desc_in = 0.250*positscale  #inches below sig line (click pt)
    return desc_in * pdfdpi

def get_locations(args,sig_page):
    # with thanks to:
    #https://matplotlib.org/3.0.0/_downloads/ginput_manual_clabel_sgskip.py
    #
    #plt.clf()
    writer = PyPDF2.PdfFileWriter()

    # create temp file and convert to png for intractive location clicking
    pdfFileName = args.pdf
    uniquetmpName = 'tmp1pageExr48csdH5ru'
    writer.addPage(sig_page)
    with open(uniquetmpName+'.pdf', 'wb') as fh:
        writer.write(fh)
    fh.close()
    
    
    ###  generate a 1-page PDF of the sig page for preview/clicking
    ##outputPDFname = args.output or "{}_signed{}".format(os.path.splitext(args.pdf))
    ##cmd = 'pdftk {:} cat {:} output {:}'.format(pdfFileName, sig_page, outputPDFname )
        ######       **** exectute command ... then:
    ##print('Executing: ', cmd)
    ##os.system(cmd)
    ## maybe no longer necessary to get 72dpi????
    cmd = 'convert -density 288 {:}.pdf -resize 25% {:}.png'.format(uniquetmpName, uniquetmpName)  # should give 72 dpi
    print('Executing: ', cmd)
    os.system(cmd)
    
    w = screenscale*8.5
    h = screenscale*11.0
    fig, ax = plt.subplots(figsize=(w,h))
 
    page_img = img.imread(uniquetmpName+'.png')
    ax.imshow(page_img)
 

    plt.setp(plt.gca(), autoscale_on=False)

    if args.date:
        tellme('Please click locations of signature and date ... then close the preview.')
    else:        
        tellme('Please click location of signature ... then close the preview.')


    #plt.waitforbuttonpress()
    if args.date:
        npts = 2
    else:
        npts = 1
    
    x = np.asarray(plt.ginput(npts,timeout=-1))
    pts = x[0]
    plt.text(pts[0],pts[1],'x',color='b')

    ptd = None
    if args.date:
        ptd = x[1]
        plt.text(ptd[0],ptd[1],'x',color='g')

    plt.show()  


    #print('You clicked (a): ', pt)
    # get int typed PDF coordinates of sig and date
    pdf_pt_s = co_xform(pts)
    pdf_pt_d = None
    if ptd is not None:
        pdf_pt_d = co_xform(ptd) 
    
    print('Sig  location:  {:}'.format(pdf_pt_s))
    if ptd is not None:
        print('Date location:  {:}'.format(pdf_pt_d))
     
    # cleanup
    os.system('rm {:}'.format(uniquetmpName+'.png'))
    os.system('rm {:}'.format(uniquetmpName+'.pdf'))
    # package results
    locs = [pdf_pt_s, pdf_pt_d]
    return locs

def get_sig_image(args):
    #
    #  TODO: open image file, read it in and DECRYPT it.
    #        c.drawImage is SUPPOSED to work with a PIL formatted
    #        image in memory but seems not to. 
    #
    #   for now only file name is returned (no encryption)
    #
    if args.signature is not None:
        img_file_path = args.signature
    else:
        ###   easier to use if repeating one sig file
        img_file_path = YOUR_FAV_SIGNATURE_IMAGE
    dims = sigbox(img_file_path) 
    print('Signature I will use is:', img_file_path, dims)
    return img_file_path, dims

def _get_tmp_filename(suffix=".pdf"):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        return fh.name

def sign_pdf(args):
    try:
        int(args.pageno)
        page_num = int(args.pageno) - 1
    except:
        page_num = 1 -1  # default is page 1
        
    print(' We are going to sign page: ', page_num+1)

    output_filename = args.output or "{}_signed{}".format(
        *os.path.splitext(args.pdf)
    )

    pdf_fh = open(args.pdf, 'rb')
    sig_tmp_fh = None

    pdf = PyPDF2.PdfFileReader(pdf_fh)
    writer = PyPDF2.PdfFileWriter()
    sig_tmp_filename = None
    
    hashkey = 'c9010ea5923339f4214c6a6eb2547b1a34a750c7ccd42980b678d61dfc9e33ac'
    args.key = hashkey
    sig_img_name, dims = get_sig_image(args)

    for i in range(0, pdf.getNumPages()):
        page = pdf.getPage(i)

        if i == page_num:  # now we are on the signature page
            # Create PDF for signature
            sig_tmp_filename = _get_tmp_filename()
            # get user to click locations
            locs = get_locations(args,page)
            (x1,y1) = locs[0]  # sig location
            y1 -= sig_descender_offset()
            if args.date:
                (x2,y2) = locs[1]  # date location
            
            c = canvas.Canvas(sig_tmp_filename, pagesize=page.cropBox)
            [width , height] = dims
            #c.drawImage(args.signature, x1, y1, width, height, mask='auto')
            c.drawImage(sig_img_name, x1, y1, width, height, mask='auto')
            if args.date:
                c.drawString(x2,y2, datetime.datetime.now().strftime("%d-%b-%Y"))
            c.showPage()
            c.save()

            # Merge PDF in to original page
            sig_tmp_fh = open(sig_tmp_filename, 'rb')
            sig_tmp_pdf = PyPDF2.PdfFileReader(sig_tmp_fh)
            sig_page = sig_tmp_pdf.getPage(0)
            sig_page.mediaBox = page.mediaBox
            page.mergePage(sig_page)

        writer.addPage(page)

    with open(output_filename, 'wb') as fh:
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
