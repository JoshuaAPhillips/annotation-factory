import xml_listgen
from xml_listgen import *
import xml.etree.ElementTree as ET
from pprint import pprint as pp

idno = xml_listgen.getIdno()
div_list = xml_listgen.divList()
facs_list = xml_listgen.facsList()
child_list = xml_listgen.childList()

"""

TO DO: 
-- turn <element>s into actual usable strings and sanitise
-- find way of zipping together lists into keys and values

def dictMaker(idno, div_list, facs_list, child_list):
    for idx, div in enumerate(div_list):

        annotation_page = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-{idx + 1}-annotations.json",
        "type": "Manifest",
        "items": []
    }
        
        for idx_2, child in enumerate(child_list):

            annotation_individual = {
            "id": f"https://raw.githubusercontent.com/JoshuaAPhillips/digital-anon/main/manifests/{idno}-annotation-{idx_2 + 1}.json",
            "type": "Annotation",
            "motivation": "Commenting",
            "target": facs_list[idx_2],
            "body": {
                "type": "TextualBody",
                "language": "en",
                "format": "text/html",
                "body": child_list[idx_2]
            }
        }
            
        annotation_page["items"].append(annotation_individual)
        
        pp(annotation_page)

dictMaker(idno, div_list, facs_list, child_list)

"""