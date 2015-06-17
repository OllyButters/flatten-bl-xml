#! /usr/bin/env python

#The punctuation is still present, so some words have e.g. a full stop attached.
#Spaces are ignored.
#Titles? are currently ignored.
#Assuming one PrintSpace per file.
#Assuming same elements/order in file - should do this on names.
#Some of the extra info - page etc could be useful?
#Not sure what the positions actually mean.
#Perhaps parse the inputs to move to lowercase and strip punctuation?

#Could easily add page info to each string too
#Could fairly easily code in the postion in a sentance.

#need to note the data type in opal
#string, string, int, int, int, int, decimal, int

import xml.etree.ElementTree as ET
import csv
import os

pages = os.listdir('data')
#print pages

#Set the output file
with open('data.csv','wb') as csvfile:
    string_file = csv.writer(csvfile)

    #opal likes a header in its csv file imports
    string_file.writerow(['id', 'content', 'hpos', 'vpos', 'width', 'height', 'wc', 'cc'])

    #cycle through each page
    for this_page in pages:
        print this_page
        
        #Parse the xml file
        #tree = ET.parse('data/002175085_01_000062.xml')
        tree = ET.parse('data/'+this_page)
        
        #Set a root
        root = tree.getroot()
        #print root
    
        
        
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
                    string_file.writerow([id, content.encode('utf-8'), hpos, vpos, width, height, wc, cc])
