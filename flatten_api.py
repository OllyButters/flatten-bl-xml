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
import sys
import json
import subprocess
import time

#Make a temp directory to put all the temp JSON and CSV files.
#os.mkdir('temp')
root_dir = os.getcwd()

books = ['hamlet']


for this_book in books:
    ########################
    #Set up the table first
    
    table_name = this_book
    
    
    #Table definition
    this_table = {'name': table_name, 'entityType': 'Book'}

    #save it as a json file
    #this_table_json_name = 'temp/'+table_name+'.json'
    this_table_json_name = 'my_table.json'
    with open(this_table_json_name, 'w') as fp:
        json.dump(this_table, fp)
        
        #Push the above json file into the opal API, this will make an empty table i.e. no variables.
        #cmd = 'opal rest -o http://192.168.56.101:8080 -u administrator -p password -m POST -ct "application/json" /datasource/bl/tables < '+this_table_json_name
        cmd = 'opal rest -o http://192.168.56.101:8080 -u administrator -p password -m POST -ct "application/json" /datasource/bl/tables < my_table.json'
        print cmd

        #works
        #cmd = 'opal rest -o http://192.168.56.101:8080 -u administrator -p password -m POST -ct "application/json" /datasource/bl/tables < my_table.json'
        #subprocess.Popen(['opal rest -o http://192.168.56.101:8080 -u administrator -p password -m POST -ct "application/json" /datasource/bl/tables < my_table.json'], shell=True)

        #this works if you exit afterwards.
        temp = subprocess.Popen([cmd], shell=True)
        temp.wait()
        print temp.returncode
        #exit()
        
        #ime.sleep(10)
        #emp.kill()

        #subprocess.call([cmd], shell=True)
        #bob=temp.check_output()

        #temp = subprocess.Popen([cmd], shell=True)

        #subprocess.call(['opal rest -o http://192.168.56.101:8080 -u administrator -p password -m POST -ct "application/json" /datasource/bl/tables < my_table.json'], shell=True)

        #os.system(cmd)

        #exit()

        #######################
        #Now do the variables
        content_var = {
            "name": "content",
            "entityType": "Book",
            "valueType": "text",
            "isRepeatable": False,
            "index": 1,
        }
        
        clean_content_var = {
            "name": "clean_content",
            "entityType": "Book",
            "valueType": "text",
            "isRepeatable": False,
            "index": 2,
        }
        
        hpos_var = {
            "name": "hpos",
            "entityType": "Book",
            "valueType": "integer",
            "isRepeatable": False,
            "index": 3,
        }
        
        vpos_var = {
            "name": "vpos",
            "entityType": "Book",
            "valueType": "integer",
            "isRepeatable": False,
            "index": 4,
        }
        
        width_var = {
            "name": "width",
            "entityType": "Book",
            "valueType": "integer",
            "isRepeatable": False,
            "index": 5,
        }
        
        height_var = {
            "name": "height",
            "entityType": "Book",
            "valueType": "integer",
            "isRepeatable": False,
            "index": 6,
        }
        
        wc_var = {
            "name": "wc",
            "entityType": "Book",
            "valueType": "decimal",
            "isRepeatable": False,
            "index": 7,
        }
        
        cc_var = {
            "name": "cc",
            "entityType": "Book",
            "valueType": "text",
            "isRepeatable": False,
            "index": 8,
        }
        
        page_var = {
            "name": "page",
            "entityType": "Book",
            "valueType": "integer",
            "isRepeatable": False,
            "index": 9,
        }
        
        all_vars=[]
        all_vars.append(content_var)
        all_vars.append(clean_content_var)
        all_vars.append(hpos_var)
        all_vars.append(vpos_var)
        all_vars.append(width_var)
        all_vars.append(height_var)
        all_vars.append(wc_var)
        all_vars.append(cc_var)
        all_vars.append(page_var)
        #print all_vars
        
        #save it as a json file
        this_variable_json_name = 'temp/'+table_name+'_vars.json'
        with open(this_variable_json_name, 'w') as fp:
            json.dump(all_vars, fp)

            #opal rest -o http://localhost:8080 -u administrator -p password -m POST -ct "application/json" /datasource/my_project/table/my_table/variables < my_variables.json
            #cmd = 'opal rest -o http://192.168.56.101:8080 -u administrator -p password -m POST -ct "application/json" /datasource/bl/table/my_table/variables < my_variables.json'
            cmd = 'opal rest -o http://192.168.56.101:8080 -u administrator -p password -m POST -ct "application/json" /datasource/bl/table/'+table_name+'/variables < '+this_variable_json_name
            os.system(cmd)


exit()

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