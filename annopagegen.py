import sys
import os
from lxml import etree
#from pprint import pprint as pp
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
  print(filename)
  return filename

def getFile(filename):

  """
  requests XML from address specified in {filename}
  """

  file = requests.get(filename)
  return file

def getRoot(file):
  response = getFile(filename)
  content = response.content
  root = etree.fromstring(content)
  print(root)
  return root

def getIdno(root):

  """
  returns idno element from TEI to use as identifier
  """

  idno = root.find('.//{http://www.tei-c.org/ns/1.0}msIdentifier/{http://www.tei-c.org/ns/1.0}idno').text
  print(idno)
  return idno

def divList(root):

  """
  returns master list of <div>s for later use
  """

  div_list = []
  divs = root.findall('.//{http://www.tei-c.org/ns/1.0}div')
  for div in divs:
    div_list.append(div)

  return div_list


def fileGen(div_list, idno):

  """
  creates 'temp' directory and saves out each <div> in a file for iterating over in further functions
  """
  if not os.path.isdir('./temp'):
    os.mkdir('./temp')
  else:
    pass

  for idx, div in enumerate(div_list):
    filename = f"./temp/{idno}-{idx + 1}.xml"
    with open(filename, "w") as f:
      f.write(etree.tostring(div, encoding="unicode"))

def divDictGen(temp_files):
  pass


def main():

  """
  Does the Thing
  """
  filename = getFilename()
  file = getFile(filename)
  root = getRoot(file)
  idno = getIdno(root)
  div_list = divList(root)
  fileGen(div_list, idno)


  

if __name__ == "__main__":
  main()



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