import sys
import os
import requests
from lxml import etree
import json

BASE_URL = 'https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/transcriptions/'

def getFilename():
  
  """
  gets name of XML file to open and appends to BASE_URL
  """

  global filename, id
  id = sys.argv[-1]
  filename = BASE_URL + id

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
  try:
    os.mkdir(f'./temp')
  except FileExistsError:
    pass

  for idx, div in enumerate(div_list):
    filename = f"./temp/{idno}-{idx + 1}.xml"
    with open(filename, "w") as f:
      f.write(etree.tostring(div, encoding="unicode"))

def divDictGen(temp_files, idno):
  """
  iterates over files in 'temp', creating a dictionary for each one
  """
  temp_file_dir = './temp'


  for filename in os.listdir(temp_file_dir):

    f = os.path.join(temp_file_dir, filename)
    if os.path.isfile(f) and f.endswith('.xml'):

      with open(f, "r") as file:
        div_dict = {}
        
        div = file.read()

        root = etree.fromstring(div)

        for p in root.findall('{http://www.tei-c.org/ns/1.0}p'):
          facs = p.get('facs')
          children = p.xpath('./*')
          div_dict[facs] = [etree.tostring(i) for i in children]

        with open(f"{f}.json", "w") as dictfile:
          json.dump(str(div_dict), dictfile)

        

def main():

  """
  Does the Thing
  """
  filename = getFilename()
  file = getFile(filename)
  root = getRoot(file)
  idno = getIdno(root)
  div_list = divList(root)
  temp_files = fileGen(div_list, idno)
  divDictGen(temp_files, idno)


  

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