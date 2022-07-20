from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

# set rootdir as the directory to loop through
rootdir = '/Users/davidwohl/tmp/worldvectorlogo.com/logo'

# create list to store title, image and source data so that writing to a file can be done outside of the loop
images = []

# walk through rootdir to access each file
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # create full path from rootdir to current file
        path_to_file = os.path.join(subdir, file)

        # set file to search through as the path from rootdir to the current file
        f = open(path_to_file)
        
        # create the full url
        src_url = "https://" + path_to_file

        # create BeautifulSoup object with current file
        soup = BeautifulSoup(f, 'html.parser')

        # set name as data from the tag "title" without the extras
        name = soup.title.string.replace(' Vector Logo - Download Free SVG Icon | Worldvectorlogo', '')

        # set src as the path to the current file -- the link where the image is obtained
        src = src_url

        #set img as the data with the class "larger"
        img = soup.find("img", {"class":"larger"})['src']

        # add current name, src and img to lists
        images.append({
            'name': name,
            'src': src,
            'img': img
        })

# set up for json dump
data = {
    'handle': "worldvectorlogo",
    'lastmodified': str(datetime.now().isoformat()),
    'name': "WorldVectorLogo",
    'provider': "remote",
    'provider_icon': "https://logosear.ch/images/remote.svg",
    'url': "https://worldvectorlogo.com/",
    'images': images,
    'logo': "https://cdn.worldvectorlogo.com/logos/worldvectorlogo.svg",
    'website': "https://worldvectorlogo.com/"
}

# path to json file
outputpath = "/Users/davidwohl/workspace/web-svg-logos/dist/worldvectorlogo.json"

outputfile = open(outputpath, 'w')

json.dump(data, outputfile, sort_keys=True, indent=2)
outputfile.close
 