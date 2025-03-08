#!/usr/bin/python
"""
What does the script do:
1. removes all CDATA sections in the .xml files to save space except Document.xml.
This is expected to be just cached data that can be recreated.
2. marks all objects to recompute in Document.xml

How to use:
1. in Freecad 'Save as Directory..." your_project_folder
2. remove cached data:
  python remove_cache.py your_project_folder/
3. do whatever (put files to git, have a life, etc.)
4. in FreeCAD 'Open Directory...'
5. recompute ('F5' or Ctrl+R)
"""

import os
import sys
from lxml import etree


def remove_cdata_from_file(file_path):
    if not file_path.endswith('.xml') or file_path.endswith('Document.xml'):
        return False
    if file_path.endswith('Document.xml'):
        return False

    # print(f'Processing file: {file_path}')
    parser = etree.XMLParser(strip_cdata=False, huge_tree=True)
    tree = etree.parse(file_path, parser)
    # root = tree.getroot()

    changed = False

    # Remove CDATA sections
    for element in tree.iter():
        element_str = etree.tostring(element, encoding='unicode')
        if "<![CDATA[" in element_str and len(element) == 0:
            element.text = ''
            print(f'Removing CDATA section from {element.tag} in {file_path}')
            changed = True

            if element.tag == 'ElementMap2' and 'count' in element.attrib:
                print(f'Setting count to 0 in <ElementMap2> of {file_path}')
                element.attrib['count'] = '0'
                element.text = ''
                changed = True

    if changed:
        # print(f'File changed: {file_path}')
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    return changed


def update_document_xml(file_path, touched_files):
    if not file_path.endswith('Document.xml'):
        return

    print(f'Updating Document.xml: {file_path}')
    parser = etree.XMLParser(strip_cdata=False)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    for element in root.xpath('//Object'):
        touched_files_basenames = map(os.path.basename, touched_files)
        if 'file' in element.attrib and element.attrib['file'] in touched_files_basenames:
            print(f'Mark {element.attrib['file']} as touched')
            element.set('Touched', '1')

    tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        targets = ['.']

    # create list of xml files
    xml_files = []
    for target in targets:
        print(target)
        if os.path.isfile(target) and target.endswith('.xml'):
            xml_files.append(target)
            # print('append', target)
        elif os.path.isdir(target):
            for root, _, files in os.walk(target):
                for file in files:
                    if file.endswith('.xml'):
                        xml_files.append(os.path.join(root, file))
                        # print('append file', file)

    # process_files
    changed_files = []
    for file in xml_files:
        if remove_cdata_from_file(file):
            changed_files.append(file)

    if changed_files:
        base_folder = os.path.dirname(xml_files[0])
        doc_path = os.path.join(base_folder, 'Document.xml')
        update_document_xml(doc_path, changed_files)
    else:
        print("No files were changed.")
