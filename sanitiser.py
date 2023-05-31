import xml.etree.ElementTree as ET
import xml_listgen
from xml_listgen import *
from pprint import pprint as pp
import re

div_list = xml_listgen.divList()
facs_list = xml_listgen.facsList()
child_list_raw = xml_listgen.childList()

def convert_pointers_to_strings(pointers):
    if isinstance(pointers, list):
        return [convert_pointers_to_strings(item) for item in pointers]
    elif isinstance(pointers, ET.Element):
        return ET.tostring(pointers).decode("utf-8")
    else:
        return pointers
    
strings = convert_pointers_to_strings(child_list_raw)
pp(facs_list)

with open('out.txt', 'w') as file:
    file.write(str(strings))