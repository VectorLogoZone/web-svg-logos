from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime

# set rootdir as the directory to loop through
rootdir = '/Users/davidwohl/tmp/logos.fandom.com/wiki'

# create list to store title, image and name data so that writing to a file can be done outside of the loop
images = []

# walk through rootdir to access each html file
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # create full path from rootdir to current html file
        path_to_file = os.path.join(subdir, file)
        
        # define function to determine if a page is invalid for logo scraping
        def invalid_page(filepath):
            if ("Category:" in filepath or "File:" in filepath or "User:" in filepath 
            or "User_talk:" in filepath or "Template:" in filepath or "Special:" in filepath 
            or "Logopedia:" in filepath or "Logopedia?" in filepath):
                return True
            else:
                return False

        # if a page is invalid as determined by the function above, skip it
        if invalid_page(path_to_file):
            continue

        # set file to search through as the path from rootdir to the current html file
        f = open(path_to_file)

        # create BeautifulSoup object with current html
        soup = BeautifulSoup(f, 'html.parser')

        # make a list containing all tags with .svg logo image urls in the document
        img_tags = soup.find_all(href=re.compile(".svg"))
        
        for img_tag in img_tags:
            img = re.sub("/revision/.*", "", str(img_tag['href']))

            # find tag with the property "og:title"
            name_tag = soup.find("meta", {"property":"og:title"})

            # if this tag does not exist, skip
            if name_tag is None:
                continue
            
            # otherwise, set name
            name = name_tag['content']

            # find tag with the property "og:url"
            src_tag = soup.find("meta", {"property":"og:url"})

            # if this tag does not exist, skip
            if src_tag is None:
                continue

            # otherwise, set src
            src = src_tag['content']

            # add current name, src and img to list
            images.append({
                'name': name,
                'src': src,
                'img': img
            })

# set up for json dump
data = {
    'handle': "logopedia",
    'lastmodified': str(datetime.now().isoformat()),
    'name': "Logopedia",
    'provider': "remote",
    'provider_icon': "https://logosear.ch/images/remote.svg",
    'url': "https://logos.fandom.com/",
    'images': images,
    'logo': "https://static.wikia.nocookie.net/logopedia/images/3/3d/Logopedia_2018.svg",
    'website': "https://logos.fandom.com/"
}

# path to json file
outputpath = "/Users/davidwohl/workspace/web-svg-logos/dist/logopedia.json"

outputfile = open(outputpath, 'w')

json.dump(data, outputfile, sort_keys=True, indent=2)
outputfile.close
 