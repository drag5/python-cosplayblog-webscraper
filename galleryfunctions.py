import requests
import linkfunctions
from bs4 import BeautifulSoup
from pathlib import Path
import os
import json
from datetime import datetime

def write_json(data, filename='gallery_data.json'):
    with open(filename,'w') as f:
        json.dump(data,f,indent=4)

def get_info (site):
    #getting all the info
    try:
        gallery_page = requests.get(site)
        gallery_soup = BeautifulSoup(gallery_page.content, 'html.parser')
        
        id = site.rsplit('/')[-2]

        name_part = gallery_soup.find("div", "POST_HEAD")
        name = str(name_part.td.string).strip()

        tags_data = gallery_soup.find("div", "taglist")
        tags_data2 = tags_data.find_all("li")
    except:
        error_msg = "Error when looking up the gallery data. Post id: " + str(id)
        linkfunctions.ErrorHandling(error_msg)
        return None

    tag_list = []

    data_number = 0
    max_num = linkfunctions.find_number_of(tags_data2)

    while data_number <= max_num:
        #to_remove = tags_data2[data_number]
        tags_data2[data_number].i.decompose()
        tag_name = tags_data2[data_number].string
        tag_list.append(str(tag_name).strip())

        data_number = data_number + 1

    

    site_info = str(site).rsplit("/")

    #getting the data into one object
    
    current_gallery = {
        'id' : id,
        'name' : name,
        'site' : site_info[2],
        'tags' : tag_list
    }

    #action depends whether the file exists or not

    if Path('gallery_data.json').is_file():
        with open('gallery_data.json') as json_file:
            current_data = json.load (json_file)
            temp = current_data['galleries']
            temp.append(current_gallery)
        
        with open('gallery_data.json', 'w') as f:
            json.dump(current_data,f,indent=4,ensure_ascii=False)

    else:
        data = {}
        data['galleries'] = []
        data['galleries'].append(current_gallery)

        with open('gallery_data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)


def get_pictures (post_URL):

    try:
        gallery_URL = post_URL
        gallery_page = requests.get(gallery_URL)

        gallery_soup = BeautifulSoup(gallery_page.content, 'html.parser')
        pictures_part = gallery_soup.find("div", "POST_BODY")

        pic_links = pictures_part.find_all("center")
    except:
        id = post_URL.rsplit('/')[-2]
        error_msg = "Error when looking pictures data. Post id: " + str(id)
        linkfunctions.ErrorHandling(error_msg)
        return None

    #checking if path from the program has the image folder
    if Path("images/").is_dir() == False:
        os.mkdir("images")

    #getting the gallery id from the link
    gallery_id = gallery_URL.rsplit('/')[-2]

    #checking if current gallery folder exists
    if Path("images/" + str(gallery_id) + '/').is_dir() == False:
        os.mkdir("images/" + str(gallery_id))

    #going through the picture links and downloading them
    i = 0
        #finding the number of pics
    i_max = linkfunctions.find_number_of(pic_links)
        #creating directory reference
    gallery_dir = Path("images/" + str(gallery_id) + "/")


    while i <= i_max :
        try:
            single_pic = pic_links[i]
            img_only = single_pic.find("img").attrs
            link_only = img_only['src']

            image_name = link_only.rsplit('/', 1)[-1]
            path_name = Path(gallery_dir / str(image_name))

            image = requests.get(link_only, allow_redirects=True)
            open(str(path_name), 'wb').write(image.content)
        except:
            id = post_URL.rsplit('/')[-2]
            error_msg = "Error when downloading pictures. Post id: " + str(id)
            linkfunctions.ErrorHandling(error_msg)
        
        i = i + 1


def Jread ():
    f = open('gallery_data.json',)
    data = json.load (f)

    for i in data['galleries']:
        print(i["id"])
    
    f.close

def checking_database (link):
    #returns True if the pictures from that post have alredy been copied
    
    if Path('gallery_data.json').is_file():

        #getting id from the link
        gallery_id = link.rsplit('/')[-2]

        file = open('gallery_data.json',)
        database = json.load (file)

        existance_flag = False

        for i in database['galleries']:
            if gallery_id == i["id"]:
                existance_flag = True

        return existance_flag
    
    else:
        return False

if __name__ == "__main__":
    Jread()