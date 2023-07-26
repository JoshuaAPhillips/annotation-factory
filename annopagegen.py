import sys
import os
import requests
from lxml import etree
from pprint import pp
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
      
  temp_file_dir = './temp'
  return temp_file_dir

def divDictGen(temp_file_dir):
  """
  iterates over files in 'temp', creating a dictionary for each one and saves out into .json
  """

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
          div_dict[facs] = [etree.tostring(i).decode('utf-8') for i in children]

        with open(f"{f}.json", "w") as dictfile:
          json.dump(div_dict, dictfile, indent=4)

def cleaner(temp_file_dir):

  """
  tidies up by deleting unnecessary .xml files
  """
  for filename in os.listdir(temp_file_dir):
    f = os.path.join(temp_file_dir, filename)
    if os.path.isfile(f) and f.endswith('.xml'):
      os.remove(f)

def manifestMaker(idno, temp_file_dir):
  """
  creates annotationPage manifests and saves to .json file
  """

  try:
    os.mkdir(f'./manifests')
  except FileExistsError:
    pass

  counter = 1

  for counter, filename in enumerate(os.listdir(temp_file_dir)):

    f = os.path.join(temp_file_dir, filename)
    with open(f, 'r') as jsonfile:
      data = json.load(jsonfile)

      keys = data.keys()
      values = data.values()

      items_list = []
      annotation_page = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-{counter + 1}-annotations.json",
        "type": "Manifest",
        "items": items_list
    }
      inner_counter = 1
      for key, value in zip(keys, values):
        annotation_individual = {
          "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-annotation_{inner_counter}.json",
          "type": "Annotation",
          "motivation": "Commenting",
          "target": [key],
          "body": {
            "type": "TextualBody",
            "language": "en",
            "format": "text/html",
            "body": [value]
          }
        }
        inner_counter += 1
        items_list.append(annotation_individual)

      with open(f"./manifests/{idno}-{counter + 1}-annotations.json", "w") as jsonfile:
        json.dump(annotation_page, jsonfile, indent=4)
        

def main():

  """
  does the Thing
  """
  filename = getFilename()
  file = getFile(filename)
  root = getRoot(file)
  idno = getIdno(root)
  div_list = divList(root)
  temp_file_dir = fileGen(div_list, idno)
  divDictGen(temp_file_dir)
  cleaner(temp_file_dir)
  manifestMaker(idno, temp_file_dir)

if __name__ == "__main__":
  main()



