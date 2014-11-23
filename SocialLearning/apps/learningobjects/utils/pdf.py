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
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            texto +=  retstr.getvalue()

    return texto            