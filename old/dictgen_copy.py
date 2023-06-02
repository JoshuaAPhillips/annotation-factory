#from bs4 import BeautifulSoup
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

  def combinedDict(self):
    div_list = self.simmer()
    
    # Iterate over each div element

    tei_dict = {}
    for div in div_list:
        div_id = div['n']  # Get the div ID
        div_dict = {}  # Create a dictionary for each div element
        
        # Find all p elements within the div
        p_elements = div.find_all('p')
        
        # Iterate over each p element
        for p in p_elements:
            facs = p.get('facs')  # Get the facs attribute
            child_para_raw = str([child for child in p if child != p('facs') and child != "\n"])

            """
            sanitises child_paras
            """
            child_para_a = re.sub(r'\n', '', child_para_raw)
            child_para_b = re.sub('(\s\s)+', '', child_para_a)
            child_para_c = re.sub(r'\\', '', child_para_b)

            # Add the facs attribute and child_para to the div dictionary
            div_dict[facs] = child_para_c
        
        # Add the div dictionary to the main TEI dictionary
        tei_dict[div_id] = div_dict

    # Print the resulting TEI dictionary
    #pp(tei_dict)

    return tei_dict
    
      

  def test(self):
    tei_dict = self.combinedDict()

    """
    with open ('{}-test.json'.format(idno.rstrip('.xml')), 'w') as file:
       json.dump(tei_dict, file, indent=4, ensure_ascii=False)
"""
test = DictGen()
test.combinedDict()
