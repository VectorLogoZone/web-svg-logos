from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

# create list to store title, source and image data so that writing to a file can be done outside of the loops
images = []

# create BeautifulSoup object with site.xml file (edited to start at the first non-logowine logo)
with open("lw-sitemap-no-start.xml") as f:
    soup = BeautifulSoup(f, "xml")

# create a list of all url tag objects
url_tags = soup.find_all('url')

# for each url tag, extract the source url first
for url_tag in url_tags:
    src = str(url_tag.loc.string)
    
    # then create a list of all image tags within that url tag (some have multiple images that we want)
    img_tags = url_tag.find_all('image:image')

    # for each image tag within the url tag, first extract the image url
    for img_tag in img_tags:
        img = str(img_tag.find('image:loc').string)

        # if the image is in .png format, we don't want to add it to the list of images
        if ".png" in img:
            continue
        # otherwise (.svg format), extract the name and add the data
        else:
            name = str(img_tag.find('image:title').string).replace(" Logo SVG", "")

            # add current name, src, and img to lists
            images.append({
                'name': name,
                'src': src,
                'img': img
            })

# set up for json dump
data = {
    'handle': "logowine",
    'lastmodified': str(datetime.now().isoformat()),
    'name': "Logowine",
    'provider': "remote",
    'provider_icon': "https://logosear.ch/images/remote.svg",
    'url': "https://www.logo.wine/",
    'images': images,
    'logo': "https://www.logo.wine/logo.svg",
    'website': "https://www.logo.wine/"
}

# path to json file
outputpath = "/Users/davidwohl/workspace/web-svg-logos/dist/logowine.json"

outputfile = open(outputpath, 'w')

json.dump(data, outputfile, sort_keys=True, indent=2)
outputfile.close
 