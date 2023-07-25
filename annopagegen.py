import sys
import os
from lxml import etree
from pprint import pprint as pp
import requests
import tempfile

BASE_URL = 'https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/transcriptions/'

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
  response = getFile()
  content = response.content
  root = etree.fromstring(content)
  return root

def getIdno():

  """
  returns idno element from TEI to use as identifier
  """
  
  root = getRoot()
  idno = root.find('.//{http://www.tei-c.org/ns/1.0}msIdentifier/{http://www.tei-c.org/ns/1.0}idno').text
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

def tempFileGen():

  """
  saves each <div> in a temp file for iterating over in further functions
  """
  div_list = divList()
  idno = getIdno()
  temp_files = []

  for div in div_list:
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
      temp_file.write(etree.tostring(div, encoding="unicode"))
      #os.system("open %s" % temp_file.name)
    temp_files.append(temp_file)
  
  return temp_files

if __name__ == "__main__":
  temp_files = tempFileGen()



"""
def dictMaker():
    root = getRoot()
    idno = getIdno()
    div_list = divList()

    for idx, div in enumerate(div_list):

        facs_list_raw = root.findall('.//{http://www.tei-c.org/ns/1.0}div/{http://www.tei-c.org/ns/1.0}p[@facs]')
        facs_list = []
        for facs in facs_list_raw:
           facs_value = facs.attrib.values()
        facs_list.append(facs_value)

        items_list = []

        annotation_page = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-{idx + 1}-annotations.json",
        "type": "Manifest",
        "items": items_list
    }
        
        for idx_2, child in enumerate(facs_list):

            annotation_individual = {
            "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-annotation-{idx_2 + 1}.json",
            "type": "Annotation",
            "motivation": "Commenting",
            "target": str(facs_list[idx_2]).strip('[').strip(']'),
            "body": {
                "type": "TextualBody",
                "language": "en",
                "format": "text/html",
                "body": "foo bar baz"
                
            }
        }
            items_list.append(annotation_individual)
        annotation_page["items"].append(annotation_individual)

        pp(annotation_page)
        
        #pp(facs_list)

dictMaker()
"""