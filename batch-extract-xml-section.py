__author__ = "Thomas Hansen (thsh1977@gmail.com)"
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2018-04-18 12:05:19 $"
__copyright__ = "Copyright (c) 2018 Thomas Hansen"
__license__ = "Python"

""" Batch extract section in XML files

Extracts specified sections from XML documents in a specified
directory

Usage: 
(1) Make sure you have the directory 'xmlfiles' containing the files
    you want to modify
(2) Run: python3 batch-extract-xml-section.py
"""

import lxml.etree as ET
import os

#ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def extract_section_from_file(data):
    e = ET.fromstring(data)
    #paragraphs = e.findall('.//{http://www.w3.org/1999/xhtml}p')
    #for p in paragraphs:
    #print (paragraphs)
    #e = ET.parse(data)
    #print(e)

    #for folder in e.findall('folder'):
    #    paragraphs = folder.iterfind('.//{http://www.w3.org/1999/xhtml}p')
    #    
    place = e.find('.//doc/meta/entry[@key="cm:title"]')
    #    chapter = folder.attrib['name']
    #    for paragraph in paragraphs:
    #        if paragraph is not None:
    folders = e.findall('folder[2]')
    paragraphs = [f.findall('.//{http://www.w3.org/1999/xhtml}p') for f in folders]
    
    return e.tag+':', place.text, [f.attrib['name'] for f in folders], paragraphs
        
def main():

    source_directory = 'xmlfiles'

    for filename in os.listdir(source_directory):

        if not filename.endswith('.xml'):
            continue

        xml_file_path = os.path.join(source_directory, filename)
        with open(xml_file_path, 'r+b') as f:
            data = f.read()
            extract = extract_section_from_file(data)
            #f.seek(0)
            print(extract)
            #f.truncate()

if __name__ == '__main__':
    main()
