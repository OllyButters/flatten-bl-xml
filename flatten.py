#! /usr/bin/env python

#The punctuation is still present, so some words have e.g. a full stop attached.
#Spaces are ignored.
#Titles? are currently ignored.
#Assuming one PrintSpace per file.
#Assuming same elements/order in file - should do this on names.

#Could easily add page info to each string too
#Could fairly easily code in the postion in a sentance.


import xml.etree.ElementTree as ET
import csv

#Parse the xml file
tree = ET.parse('002175085_01_000062.xml')

#Set a root
root = tree.getroot()
#print root

#Set the output file
with open('data.csv','wb') as csvfile:
    string_file = csv.writer(csvfile)

    #opal likes a header in its csv file imports
    string_file.writerow(['id', 'content', 'hpos', 'vpos', 'width', 'height', 'wc', 'cc'])

    #Cycle through the root from the
    #<Layout><Page><PrintSpace> part. Assume these line up with [2][0][4]
    for this_textblock in root[2][0][4].findall('TextBlock'):
        for this_textline in this_textblock.findall('TextLine'):
            for this_string in this_textline.findall('String'):
                id = this_string.get('ID')
                hpos = this_string.get('HPOS')
                vpos = this_string.get('VPOS')
                width = this_string.get('WIDTH')
                height = this_string.get('HEIGHT')
                content = this_string.get('CONTENT')
                wc = this_string.get('WC')
                cc = this_string.get('CC')
                print content, id, hpos, vpos, width, height, wc, cc
                string_file.writerow([id, content, hpos, vpos, width, height, wc, cc])
