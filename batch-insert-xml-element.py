__author__ = "Thomas Hansen (thsh1977@gmail.com)"
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2018-04-18 12:05:19 $"
__copyright__ = "Copyright (c) 2018 Thomas Hansen"
__license__ = "Python"

""" Batch insert element in XML files

Inserts an XML element 'abstract' at a specified place

Usage: 
(1) Make sure you have the directory 'xmlfiles' containing the files
    you want to modify
(2) Run: python3 batch-insert-xml-element.py
"""

from xml.etree import ElementTree as ET
import os

ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def edit_xml_file(data):
    e = ET.fromstring(data)

    for file_element in e.findall('tei:teiHeader//tei:profileDesc', ns):
        abstract = ET.Element('abstract')
        abstract.text = 'nil'
        file_element.insert(1, abstract)

    xmlstr = ET.tostring(e, encoding='utf-8')
    return xmlstr


def main():

    source_directory = 'xmlfiles'

    for filename in os.listdir(source_directory):

        if not filename.endswith('.xml'):
            continue

        xml_file_path = os.path.join(source_directory, filename)
        with open(xml_file_path, 'r+b') as f:
            data = f.read()
            fixed_data = edit_xml_file(data)
            f.seek(0)
            f.write(fixed_data)
            f.truncate()

if __name__ == '__main__':
    main()
