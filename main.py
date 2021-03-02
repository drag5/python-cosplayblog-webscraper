import requests
import linkfunctions
import galleryfunctions
from bs4 import BeautifulSoup
from pathlib import Path
import os
from datetime import datetime



URL = "https://mpzerocos.exblog.jp/"
print ("Up to what page you want to download?")
finish_page = input()

current_page = 0

while int(current_page) < int(finish_page):

    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
    except:
        error_msg = "Error when loading the page. Page: " + str(int(current_page) + 1)
        linkfunctions.ErrorHandling(error_msg)
        break

    #getting rid off the unnecessary first post
    try:
        if linkfunctions.SkippingCheck(soup) == True:
                
            unwanted = soup.find("div", class_="POST")
            soup.find("div", class_="POST").decompose()
    except:
        error_msg = "Error when looking up the posts. Page: " + str(int(current_page) + 1)
        linkfunctions.ErrorHandling(error_msg)
        break

    #preparing list of galleries
    all_posts = soup.find_all("div", "POST")
    gallery_list = linkfunctions.LinksToGaleries(all_posts)

    #finding number of posts on the site
    no_posts = linkfunctions.find_number_of(all_posts)
    current_post = 0

    while current_post <= no_posts :

        if galleryfunctions.checking_database(gallery_list[current_post]) == False :
            galleryfunctions.get_pictures(gallery_list[current_post])
            galleryfunctions.get_info(gallery_list[current_post])
        
        current_post = current_post + 1

    current_page = linkfunctions.CurrentPage(soup)
    
    next_page = linkfunctions.NextPageCheck(soup) 
    if next_page is not None:
        URL = next_page
    else:
        print ("Reached the end!")
        break
