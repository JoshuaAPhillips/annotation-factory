from lxml import etree as ET
import sys
import requests
from pprint import pprint as pp
import io

BASE_URL = 'https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/transcriptions/'

namespaces = {
    'tei': 'http://www.tei-c.org/ns/1.0',
}

def getFilename():
  
  """
  gets name of XML file to open and appends to BASE_URL
  """

  global filename, id
  id = sys.argv[-1]
  filename = BASE_URL + id
  return filename

def getFile():

  """
  requests XML from address specified in {filename}
  """

  filename = getFilename()

  r = requests.get(filename)
  return r

def getRoot():

  """
  gets root node from XML for further processing
  """
  response = getFile()
  content = response.text
  content_bytes = content.encode('utf-8')
  content_file = io.BytesIO(content_bytes)
  tree = ET.parse(content_file)
  root = tree.getroot()
  return root

def getIdno():

  """
  returns idno element from TEI to use as identifier
  """
  
  root = getRoot()
  idno = root.find(".//tei:idno", namespaces=namespaces)
  return idno

def divList():

  """
  returns master list of <div>s for later use
  """

  root = getRoot()

  div_list = []
  divs = root.findall('.//tei:div', namespaces=namespaces)
  for div in divs:
    div_list.append(div)
  #print(div_list)
  return div_list

def facsList():

  """
  returns nested list of <p> elements with @facs attributes
  -- these are arranged by parent <div>
  -- intended for use as target for IIIF annotation
  """

  root = getRoot()
  div_list = divList()
  facs_list = []

  for div in div_list:

    inner_list = []
    for child in div:
      facs = root.find('.//tei:div/tei:p[@facs]', namespaces=namespaces)
      inner_list.append(facs.attrib["facs"])
    facs_list.append(inner_list)

  return facs_list

def childList():
  
  """
  returns nested list of children for each <p> element with @facs attribute
  -- arranged first by <div> then by <p>
  -- intended for use as TextualBody for IIIF annotation
  """
  root = getRoot()
  div_list = divList()
  facs_list = facsList()

  child_list = []
  elements = root.findall('.//tei:p[@facs]', namespaces=namespaces)

  for element in elements:
    inner_list = []
    descendants = element.iterdescendants()
    for descendant in descendants:
        tag = descendant.tag
        text = descendant.text

        content = f"<{tag}>{text}</{tag}>"

        inner_list.append(content)
    child_list.append(inner_list)
  pp(child_list)
        

getIdno()
divList()
facsList()
childList()



