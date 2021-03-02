import re
from bs4 import BeautifulSoup
from datetime import datetime

#temporary
import requests


def prepare_link (post):
    #prepares the link to the gallery from a post
    raw_link = re.search("(?P<url>https?://[^\s]+)", str(post)).group("url")
    #processed_link = raw_link[0:len(raw_link)-2]
    position = str(raw_link).find('"')
    processed_link = str(raw_link)[:position]

    return processed_link

def find_number_of (all_posts):
    #find number of posts on the page (number of the last one)
    i = 0
    existance = True

    while existance == True:

        try:
            single_post = all_posts[i]
        except:
            existance = False
            i = i - 2
        
        i = i + 1
    
    return i

def LinksToGaleries (all_posts):
    link_list = []
    i = 0
    last = find_number_of(all_posts)

    while i <= last :
        link_list.append(prepare_link(all_posts[i]))
        i = i + 1
    
    return link_list


def SkippingCheck (soup):
    #returns true, if it's the first page
    navi = soup.find("div", "pagerNavLink")
    page = navi.find("span", "current")

    if str(page.string) == "1":
        return True
    else:
        return False


def NextPageCheck (soup):
    #returns None if there is no page, and a link if there is
        navi = soup.find("div", "pagerNavLink")
        next = navi.find("span", "nextpage")

        try:
            raw_link = re.search("(?P<url>https?://[^\s]+)", str(next)).group("url")
        except:
            return None

        position = str(raw_link).find('"')
        link = str(raw_link)[:position]

        return link

def CurrentPage(soup):
    #returns number of current page

    navi = soup.find("div", "pagerNavLink")
    page = navi.find("span", "current")

    return str(page.string) 

def ErrorHandling(ErrorMsg):
    dateTimeObj = datetime.now()
    ts = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    error = str(ts) + ": " + str(ErrorMsg) + "\n"
    with open("log.txt", "a+") as bugreport:
        bugreport.write(str(error))





if __name__ == "__main__":
    URL = "https://mpzerocos.exblog.jp/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    NextPageCheck(soup) 


