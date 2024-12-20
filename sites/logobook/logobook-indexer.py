from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

# set rootdir as the directory to loop through
rootdir = '/Users/davidwohl/tmp/www.logobook.com/logo'

# create list to store title, image and name data so that writing to a file can be done outside of the loop
images = []

# walk through rootdir to access each index.html
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # create full path from rootdir to current index.html file
        path_to_file = os.path.join(subdir, file)

        # set file to search through as the path from rootdir to the current index.html file
        f = open(path_to_file)

        # create the full url, taking out index.html from the file name
        src_url = "http://" + path_to_file.replace('index.html', '')

        # create BeautifulSoup object with current index.html
        soup = BeautifulSoup(f, 'html.parser')

        # set name as the data with the name "twitter:title"
        name = soup.find("meta", {"name":"twitter:title"})['content'].replace(' - Logobook', '')

        # set src as the path to the current file -- the link where the image is obtained
        src = src_url

        #set img_url as the data with the name "twitter:image"
        img_url = soup.find("meta", {"name":"twitter:image"})['content']

        # edit img_url to work in proxy
        img = img_url.replace('http://www.logobook.com', 'https://proxy.svg.zone/logobook')

        # add current name, src and img to lists
        images.append({
            'name': name,
            'src': src,
            'img': img
        })

# set up for json dump
data = {
    'handle': "logobook",
    'lastmodified': str(datetime.now().isoformat()),
    'name': "Logobook",
    'provider': "remote",
    'provider_icon': "https://logosear.ch/images/remote.svg",
    'url': "http://www.logobook.com/",
    'images': images,
    'logo': "https://proxy.svg.zone/logobook/wp-content/themes/bespoke_1-1/images/logomark.svg",
    'website': "http://www.logobook.com/"
}

# path to json file
outputpath = "/Users/davidwohl/workspace/web-svg-logos/dist/logobook.json"

outputfile = open(outputpath, 'w')

json.dump(data, outputfile, sort_keys=True, indent=2)
outputfile.close
