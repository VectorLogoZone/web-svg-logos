from bs4 import BeautifulSoup
import os

# set rootdir as the directory to loop through
rootdir = 'www.logobook.com/logo'

# create lists to store title and image data so that writing to a file can be done outside of the loop
title_list = []
image_list = []

# walk through rootdir to access each index.html
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        # create full path from rootdir to current index.html file
        path_to_file = os.path.join(subdir, file)

        # set file to search through as the path from rootdir to the current index.html file
        f = open(path_to_file)

        # create BeautifulSoup object with current index.html
        soup = BeautifulSoup(f, 'html.parser')

        # set title as the data with the name "twitter:title"
        title = soup.find("meta", {"name":"twitter:title"})['content']

        #set image as the data with the name "twitter:image"
        image = soup.find("meta", {"name":"twitter:image"})['content']

        # add current title and image to lists
        title_list.append(title)
        image_list.append(image)

# open logobook-data.txt in static/logosearch and write title and image data to it
with open("/Users/davidwohl/workspace/logosearch/static/logosearch/logobook-data.txt", "w") as file:
    # as the lengths of title_list and image_list must be the same, we can go through them both concurrently
    for x in range(len(title_list)):
        file.write(str(title_list[x]) + "\n" + str(image_list[x]) + "\n\n")   