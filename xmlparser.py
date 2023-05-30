import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import sys

BASE_URL = 'https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/transcriptions/'

class xmlParser:

  def __init__(self) -> None:
    return

  def getFilename(self):
    """
    gets name of XML file to open and appends to BASE_URL
    """
    global filename, idno
    idno = sys.argv[-1]
    filename = BASE_URL + idno
    return filename

  def getFile(self):

    """
    requests XML from address specified in {filename}
    """

    filename = self.getFilename()

    print(f"Loading file from URL: {filename}")
    r = requests.get(filename)
    return r

  def makeSoup(self):

    """
    returns text of requested file as a BeautifulSoup object
    """

    r = self.getFile()
    global soup
    soup = BeautifulSoup(r.text, features="xml")
    return soup

test = xmlParser()
test.makeSoup()