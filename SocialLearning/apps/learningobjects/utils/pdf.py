from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter

# Open the url provided as an argument to the function and read the content
import urllib2
import requests
from urllib2 import Request


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re
import csv


def convert_pdf_to_html(url):

    r = requests.head(url)
    r.headers["content-type"]

    if 'application/pdf' in r.headers["content-type"]:

        r = requests.get(url)

        # Cast to StringIO object
        from StringIO import StringIO
        memory_file = StringIO(r.content)

        # Create a PDF parser object associated with the StringIO object
        parser = PDFParser(memory_file)

        # Create a PDF document object that stores the document structure
        document = PDFDocument(parser)

        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0 #is for all
        caching = True
        pagenos=set()

        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)

        device.close()
        str = retstr.getvalue()
        retstr.close()
        return str

def extract_pdf(url):

    r = requests.head(url)
    r.headers["content-type"]

    if 'application/pdf' in r.headers["content-type"]:

        r = requests.get(url)

        # Cast to StringIO object
        from StringIO import StringIO
        memory_file = StringIO(r.content)

        # Create a PDF parser object associated with the StringIO object
        parser = PDFParser(memory_file)

        # Create a PDF document object that stores the document structure
        document = PDFDocument(parser)

        # Define parameters to the PDF device objet 
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        codec = 'utf-8'

        # Create a PDF device object
        device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)

        # Create a PDF interpreter object
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Process each page contained in the document
        texto = ''
        page_no = 1
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            texto +=  retstr.getvalue()
            page_no += 1

            if page_no > 5:
                break

    return texto            