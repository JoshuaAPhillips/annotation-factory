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
  
  """
  Try functions to get lists of facs attribs, children, etc. and then call in generator function at end
  """
  
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

      div_children = div.find_all('p')
"""
      for child in div_children:
        annotation = {
            "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-{idx + 1}-annotation-{idx + 1}.json",
            "type": "Annotation",
            "motivation": "Commenting",
            "target": facs_list[idx],
            "body": {
                "type": "TextualBody",
                "language": "en",
                "format": "text/html",
                "body": child_list[idx]
            }
        }

        annotation_page["items"].append(annotation)
      manifest_list.append(annotation_page)
    pp(manifest_list)
"""
test = DictGen()
test.manifestGen()
