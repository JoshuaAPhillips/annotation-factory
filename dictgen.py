from bs4 import BeautifulSoup
from pprint import pprint as pp
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
  
  def facs_dict(self):
    div_list = self.simmer()
    facs_dict = {}

    for div in div_list:
        parent_facs = div.get('n')
        children = div.find_all(attrs={'facs': True})
        
        child_facs_list = []
        
        for child in children:
            child_facs_list.append(child.get('facs'))
        
        facs_dict[parent_facs] = child_facs_list
    #pp(facs_dict)
    return facs_dict

  def child_dict(self):
     div_list = self.simmer()

     for div in div_list:
        pass

  def test(self):
    div_list = self.simmer()
    #pp(div_list)

test = DictGen()
test.facs_list()
