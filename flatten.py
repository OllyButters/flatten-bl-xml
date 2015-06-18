#! /usr/bin/env python

#Olly Butters
#18/6/15

#First stab at taking one of the BL XML files and flattening it into a CSV file to 
#push into opal.

#The punctuation is still present, so some words have e.g. a full stop attached.
#Spaces are ignored.
#Titles? are currently ignored.
#Assuming one PrintSpace per file.
#Assuming same elements/order in file - should do this on names.
#Not sure what the positions actually mean.

#Could fairly easily code in the postion in a sentance.

#need to note the data type in opal
#id,     content, clean_content, hpos, vpos, width, height, wc,      cc,     page
#string, string,  string,        int,  int,  int,   int,    decimal, string, int

import xml.etree.ElementTree as ET
import csv
import os

#Get the list of files in the directory
pages = os.listdir('data')

#Set the output file
with open('data.csv','wb') as csvfile:
    string_file = csv.writer(csvfile)

    #opal likes a header in its csv file imports
    string_file.writerow(['id', 'content', 'clean_content', 'hpos', 'vpos', 'width', 'height', 'wc', 'cc', 'page'])

    #cycle through each page
    for this_page in pages:
        print this_page
        
        #Parse the xml file
        tree = ET.parse('data/'+this_page)
        
        #Set a root
        root = tree.getroot()
        
        #Grab the page number
        page = root[2][0]
        page_number = page.get('ID')

        #The page number starts with a P, get rid of this
        page_number = page_number.strip('P')
        
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
                    
                    #Clean the content, i.e. the actual words. 
                    #Lets make it all lower case.
                    clean_content = content.lower()
                    
                    #Get rid of punctuation
                    clean_content = clean_content.strip('.,!?";:-')

                    #Output the information to screen and file
                    print content, clean_content, id, hpos, vpos, width, height, wc, cc, page_number
                    string_file.writerow([id, content.encode('utf-8'), clean_content.encode('utf-8'), hpos, vpos, width, height, wc, cc, page_number])
