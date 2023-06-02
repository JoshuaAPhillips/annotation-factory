import requests
import xml.etree.ElementTree as ET
import sys
from pprint import pprint as pp
import re


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

    r = requests.get(filename)
    return r
  
  def getRoot(self):
    response = self.getFile()
    content = response.content
    root = ET.fromstring(content)

    #print(root)

    return root
  
  def getIdno(self):
    root = self.getRoot()
    idno = root.find('.//{http://www.tei-c.org/ns/1.0}msIdentifier/{http://www.tei-c.org/ns/1.0}idno').text
    return idno
  
  def divList(self):
    root = self.getRoot()

    div_list = []
    divs = root.findall('.//{http://www.tei-c.org/ns/1.0}div')
    for div in divs:
      div_list.append(div)
    return div_list
  
  def facsList(self):
    root = self.getRoot()
    div_list = self.divList()
    facs_list = []

    for div in div_list:
      inner_list = []
      for child in div:
        facs = root.find('.//{http://www.tei-c.org/ns/1.0}div/{http://www.tei-c.org/ns/1.0}p[@facs]')
        inner_list.append(facs.attrib["facs"])
      facs_list.append(inner_list)
    return facs_list
  
  def childList(self):
    div_list = self.divList()

    child_list_raw = []

    for div in div_list:
      inner_list = []

      for p in div.findall('.//{http://www.tei-c.org/ns/1.0}p[@facs]'):
        children = p.findall('.//{http://www.tei-c.org/ns/1.0}*')
        for i in children:
          children_strings = ET.tostring(i, encoding="unicode")
          inner_list.append(children_strings)
      child_list_raw.append(inner_list)

    with open ('out.txt', 'w') as file:
      file.write(str(child_list_raw))


test = xmlParser()
test.childList()