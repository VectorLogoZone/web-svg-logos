from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime

# set rootdir as the directory to loop through
rootdir = '/Users/davidwohl/tmp/brandeps.com/logo'

# create list to store title, image and name data so that writing to a file can be done outside of the loop
images = []

# walk through rootdir to access each page
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # create full path from rootdir to current page
        path_to_file = os.path.join(subdir, file)

        # set file to search through as the path from rootdir to the current page
        f = open(path_to_file)

        # create BeautifulSoup object with current page
        soup = BeautifulSoup(f, 'html.parser')

        # store link tag with as="image" in img_tag
        img_tag = soup.find("link", {"as":"image"})
        
        # if this tag doesn't exist, this page is a category page, so we should skip
        if img_tag is None:
            continue

        # get href attribute from this tag, store as img
        img = img_tag['href']

        # extract the source url from link tag with rel="canonical"
        src = soup.find("link", {"rel":"canonical"})['href']

        # find name within the title tag (removes everything after the title, including an 02)
        name = re.sub(' logo vector.*', '', str(soup.title.string))

        # add current name, src and img to list
        images.append({
            'name': name,
            'src': src,
            'img': img
        })

# set up for json dump
data = {
    'handle': "brandeps",
    'lastmodified': str(datetime.now().isoformat()),
    'name': "BrandEPS",
    'provider': "remote",
    'provider_icon': "https://logosear.ch/images/remote.svg",
    'url': "https://brandeps.com/",
    'images': images,
    'logo': "https://brandeps.com/logo-download/B/BrandEPS-logo-vector-01.svg",
    'website': "https://brandeps.com/"
}

# path to json file
outputpath = "/Users/davidwohl/workspace/web-svg-logos/dist/brandeps.json"

outputfile = open(outputpath, 'w')

json.dump(data, outputfile, sort_keys=True, indent=2)
outputfile.close
 