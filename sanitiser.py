import xml.etree.ElementTree as ET
import xml_listgen
from xml_listgen import *
from pprint import pprint as pp
import re

div_list = xml_listgen.divList()
facs_list = xml_listgen.facsList()
child_list_raw = xml_listgen.childList()

ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

def childToMessyString():
    
    pass

childToMessyString()