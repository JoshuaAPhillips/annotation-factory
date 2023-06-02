import sys
from lxml import etree as ET, objectify
from pprint import pprint as pp
import requests

BASE_URL = 'https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/transcriptions/'

"""
idno = xml_listgen.getIdno()
div_list = xml_listgen.divList()
facs_list = xml_listgen.facsList()
child_list = xml_listgen.childList()
"""

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
  requests XML fromg address specified in {filename}
  """

  filename = getFilename()

  r = requests.get(filename)
  return r

def getRoot():
  response = getFile()
  content = response.content
  root = ET.fromstring(content)
  return root

def getIdno():

  """
  returns idno element from TEI to use as identifier
  """
  
  root = getRoot()
  idno = root.find('.//{http://www.tei-c.org/ns/1.0}msIdentifier/{http://www.tei-c.org/ns/1.0}idno').text
  print(idno)
  return idno

def divList():

  """
  returns master list of <div>s for later use
  """

  root = getRoot()

  div_list = []
  divs = root.findall('.//{http://www.tei-c.org/ns/1.0}div')
  for div in divs:
    div_list.append(div)

  return div_list


def dictMaker():
    root = getRoot()
    idno = getIdno()
    div_list = divList()

    for idx, div in enumerate(div_list):

        facs_list = []
        facs = root.find('.//{http://www.tei-c.org/ns/1.0}div/{http://www.tei-c.org/ns/1.0}p[@facs]').attrib.values()
        facs_list.append(facs)

        annotation_page = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-{idx + 1}-annotations.json",
        "type": "Manifest",
        "items": items[idx]

                            }
        for idx_2, child in enumerate(facs_list):
            items = []

            annotation_individual = {
            "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-annotation-{idx_2 + 1}.json",
            "type": "Annotation",
            "motivation": "Commenting",
            "target": facs_list[idx_2],
            "body": {
                "type": "TextualBody",
                "language": "en",
                "format": "text/html",
                "body": "foo bar baz"

            }
        }        
        items.append(annotation_individual)
        annotation_page["items"].append([i for i in items])
        
        pp(annotation_page)

dictMaker()