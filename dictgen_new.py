from bs4 import BeautifulSoup
from pprint import pprint as pp
import re
import json
import xmlparser
from xmlparser import *

class DictGen:
    
  def __init__(self) -> None:
    filename = xmlparser.filename
    idno = xmlparser.idno
    soup = xmlparser.soup

  def simmer(self):
    global div_list
    div_list = soup.find_all('div')
    return div_list
  
  def manifestGen(self):
    div_list = self.simmer()
    manifest_list = []

    for idx, div in enumerate(div_list):

      annotation_page = {
          "@context": "http://iiif.io/api/presentation/3/context.json",
          "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-{idx + 1}-annotations.json",
          "type": "Manifest",
          "items": []
      }
    
      manifest_list.append(annotation_page)
    pp(manifest_list)

test = DictGen()
test.manifestGen()
