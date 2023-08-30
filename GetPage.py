import requests
from bs4 import BeautifulSoup
import re

#link = "https://www.alldeaf.com/forums/introduce-yourself.45"

def GetPage(link):
    try:   
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        page = str(soup.find_all(class_="pageNav-page")[-1])
        page_num = re.compile(r'.*page-(\d*?)">').findall(page)[0]
        #print(int(page_num))
    except:
        raise Exception('Error in handling: ' + link)
    return int(page_num)
    