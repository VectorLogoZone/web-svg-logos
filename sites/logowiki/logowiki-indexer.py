from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

# set rootdir as the directory to loop through
rootdir = '/Users/davidwohl/tmp/logowiki.net/logo'

# create list to store title, image and name data so that writing to a file can be done outside of the loop
images = []

# walk through rootdir to access each file
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # create full path from rootdir to current file
        path_to_file = os.path.join(subdir, file)

        # set file to parse through as the path from rootdir to the current logo file
        f = open(path_to_file)

        # create BeautifulSoup object with current file
        soup = BeautifulSoup(f, 'html.parser')

        # find the image tag with the 600px width style attribute (used twice later)
        img_tag = soup.find("img", {"style":"width: 600px;"})

        # set name as the title attribute this image tag
        name = img_tag['title']

        # set src as the data with the rel attribute "canonical" in the a link tag
        src = soup.find("link", {"rel":"canonical"}).get('href')

        # set img as the link to the logowiki home page + the src attribute of the image tag described above
        img = "https://logowiki.net" + img_tag['src']

        # add current name, src and img to list
        images.append({
            'name': name,
            'src': src,
            'img': img
        })

# set up for json dump
data = {
    'handle': "logowiki",
    'lastmodified': str(datetime.now().isoformat()),
    'name': "LogoWiki",
    'provider': "remote",
    'provider_icon': "https://logosear.ch/images/remote.svg",
    'url': "https://logowiki.net/",
    'images': images,
    # logo on home page is a .png
    #'logo': "",
    'website': "https://logowiki.net/"
}

# path to json file
outputpath = "/Users/davidwohl/workspace/web-svg-logos/dist/logowiki.json"

outputfile = open(outputpath, 'w')

json.dump(data, outputfile, sort_keys=True, indent=2)
outputfile.close
 