from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime

# set rootdir as the directory to loop through
# NOTE: there is no logo directory for iconape, so I made my own and used select all to move the logos into it
rootdir = '/Users/davidwohl/tmp/iconape.com/logo'

# create list to store title, source and image data so that writing to a file can be done outside of the loops
images = []

# walk through rootdir to access each html file
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # create full path from rootdir to current index.html file
        path_to_file = os.path.join(subdir, file)

        # set file to search through as the path from rootdir to the current html file
        f = open(path_to_file)
        # printing the file path as making the BeautifulSoup would sometimes cause errors
        print(path_to_file)

        # create BeautifulSoup object with current index.html
        soup = BeautifulSoup(f, 'html.parser')

        # to isolate the tag with the .svg link that we want, we can search for "/svg/" in the href attr 
        img_tag = soup.find(href=re.compile("/svg/"))

        # if this tag does not exist, there is no .svg image in the page, so skip
        if img_tag is None:
            continue

        # otherwise, extract img url from the above tag
        img = img_tag['href']

        # extract source link from 'link' tag with rel="canonical"
        src = soup.find("link", {"rel":"canonical"})['href']

        # find name within 'meta' tag with itemprop="name"
        name = re.sub('( Logo)?', '', soup.find("meta", {"itemprop":"name"})['content'])

        # add current name, src, and img to lists
        images.append({
            'name': name,
            'src': src,
            'img': img
        })

# set up for json dump
data = {
    'handle': "iconape",
    'lastmodified': str(datetime.now().isoformat()),
    'name': "IconApe",
    'provider': "remote",
    'provider_icon': "https://logosear.ch/images/remote.svg",
    'url': "https://iconape.com/",
    'images': images,
    'logo': "https://iconape.com/wp-content/themes/svvvg/v01/imgs/logo.svg",
    'website': "https://iconape.com/"
}

# path to json file
outputpath = "/Users/davidwohl/workspace/web-svg-logos/dist/iconape.json"

outputfile = open(outputpath, 'w')

json.dump(data, outputfile, sort_keys=True, indent=2)
outputfile.close
 