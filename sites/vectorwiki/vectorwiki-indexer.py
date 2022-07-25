from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime

# create list to store title, source and image data so that writing to a file can be done outside of the loops
images = []

# create BeautifulSoup object with sitemap.xml file
with open("vectorwiki-sitemap.xml") as f:
    soup = BeautifulSoup(f, "xml")

# create a function to check if a tag is a url tag and that tag's loc is a logo page (contains /logo/), not a directory
def is_logo_page(tag):
    return tag.name == 'url' and "/logo/" in str(tag.loc.string)

# create a list of all url tags representing logo pages using above function
url_tags = soup.find_all(is_logo_page)

# for each url tag, find the image:image tag first
for url_tag in url_tags:
    img_tag = url_tag.find('image:image')

    # check if the this tag's image:loc tag string contains .svg -- if not, skip after printing
    img_loc = str(img_tag.find('image:loc').string)
    if ".svg" not in img_loc:
        continue

    # otherwise, extract the image:loc text from this tag as img
    img = img_loc

    # extract image:title from this tag as name
    name = re.sub(' SVG (Vector )?Logo', '' , str(img_tag.find('image:title').string))

    # then get src from the text of the url tag's loc tag (done down here in case an element is skipped)
    src = url_tag.loc.string

    # add current name, src, and img to lists
    images.append({
                'name': name,
                'src': src,
                'img': img
            })

# set up for json dump
data = {
    'handle': "vectorwiki",
    'lastmodified': str(datetime.now().isoformat()),
    'name': "Vector Wiki",
    'provider': "remote",
    'provider_icon': "https://logosear.ch/images/remote.svg",
    'url': "https://vectorwiki.com/",
    'images': images,
    # 'logo': "",
    'website': "https://vectorwiki.com/"
}

# path to json file
outputpath = "/Users/davidwohl/workspace/web-svg-logos/dist/vectorwiki.json"

outputfile = open(outputpath, 'w')

json.dump(data, outputfile, sort_keys=True, indent=2)
outputfile.close
 