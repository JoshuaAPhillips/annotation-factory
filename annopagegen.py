import sys
import os
import requests
import logging
from lxml import etree
from pprint import pp
import json
import natsort
import shutil
import re

BASE_URL = 'https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/transcriptions/'

logging.basicConfig(level=logging.INFO)

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
  logging.info(f'Downloading {id} from {filename}...')
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

  logging.info('Generating temporary files...')

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

def xmlCleaner(temp_file_dir):

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

  regex = r'/(\d+,\d+,\d+,\d+)'

  try:
    os.mkdir(f'./{idno}-manifests')
  except FileExistsError:
    pass

  file_list = natsort.natsorted(os.listdir(temp_file_dir))
  #pp(file_list)

  manifest_list = []

  for counter, filename in enumerate(file_list):

    f = os.path.join(temp_file_dir, filename)
    with open(f, 'r') as jsonfile:
      data = json.load(jsonfile)

      keys = data.keys()
      values = data.values()

      items_list = []
      annotation_page = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/annotations/{idno}-annotations/{idno}-{counter + 1}-annotations.json",
        "type": "AnnotationPage",
        "items": items_list
    }
      inner_counter = 1
      for key, value in zip(keys, values):

        keySanitiser = lambda key: re.sub(r'(/iiif/2/[^/]+/[^/]+)/([^/]+/full/0/default.tif)$', r'\1#xywh=\2', key).strip('/full/0/default.tif')


        annotation_individual = {
          "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-annotation#{inner_counter}.json",
          "type": "Annotation",
          "motivation": "commenting",
          "target": keySanitiser(key),
          "body": {
            "type": "TextualBody",
            "language": "en",
            "format": "text/html",
            "value": value
          }
        }
        inner_counter += 1
        items_list.append(annotation_individual)
      

      manifest_list.append(annotation_page)

  logging.info(f'Generating IIIF AnnotationPage manifests for {filename}...')

  return manifest_list

def jsonSave(idno, manifest_list):

  for file_counter, annotation_page in enumerate(manifest_list):
    with open(f"./{idno}-manifests/{idno}-{file_counter +1}-annotations.json", "w") as jsonfile:
      
      json.dump(annotation_page, jsonfile, indent=4)
  logging.info(f'Saving {idno} manifests to JSON...')

def cleanupFinal():
  path = './temp'
  try:
    shutil.rmtree(path)
  except OSError as e:
    logging.error(f"Error: {e.filename} - {e.strerror}.")

  logging.info('Cleaning up temporary files...')

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
  xmlCleaner(temp_file_dir)
  manifest_list = manifestMaker(idno, temp_file_dir)
  jsonSave(idno, manifest_list)
  cleanupFinal()
  print(f'AnnotationPage manifests for {filename} successfully generated')

if __name__ == "__main__":
  main()



