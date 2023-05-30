from bs4 import BeautifulSoup
from pprint import pprint as pp
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
  
  def getN(self):
    div_list = self.simmer()

    n_list = []
    for div in div_list:
       n = div.get('n')
       n_list.append(n)

    return n_list
    #pp(n_list)
  
  def facsDict(self):
    div_list = self.simmer()
    n_list = self.getN()

    facs_dict = {}

    for idx, div in enumerate(div_list):
        
        n_item = n_list[idx]
        
        children = div.find_all(attrs={'facs': True})
        
        child_facs_list = []
        
        for child in children:
            child_facs_list.append(child.get('facs'))
        
        facs_dict[n_item] = child_facs_list
    
    return facs_dict

  def childDict(self):
    div_list = self.simmer()
    n_list = self.getN()

    child_dict = {}

    for idx, div in enumerate(div_list):
      n_item = n_list[idx]

      p_children = div.find_all('p')
      p_children_list = []
      for child in p_children:
        if child.text != '\n':
          p_children_list.append(child)
        else:
          pass

      child_dict[n_item] = p_children_list

    return child_dict

  def combinedDict(self):
    facs_dict = self.facsDict()
    child_dict = self.childDict()
    n_list = self.getN()

    combined_dict = {}

    for key, value in facs_dict.items():
      combined_dict = {key: value for key, value in zip(facs_dict.items())}

    return combined_dict
    
      

  def test(self):
    facs_dict = self.facsDict()
    child_dict = self.childDict()
    combined_dict = self.combinedDict()
    
    #with open('test.txt', 'w') as out:
      #pp(combined_dict, stream=out)


test = DictGen()
test.combinedDict()
