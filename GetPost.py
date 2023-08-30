import requests
from bs4 import BeautifulSoup
import re
import numpy as np

#post = "https://www.alldeaf.com/threads/hi-guys-an-hoh-girl-with-an-interesting-story-here.136409/"

def GetPost(post):
    try:
        headers = {
        'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
    }
        r = requests.get(post,headers=headers, timeout=15)
        soup = BeautifulSoup(r.content, 'html.parser')

        datetime = soup.find_all(class_="u-dt")[0]
        time = re.compile(r'.*datetime="(.*?)"').findall(str(datetime))[0]
        #print('dt')

        user = soup.find_all(class_="message-userExtras")[0]
        user_info = re.compile(r'.*<dd>(.*?)</dd>').findall(str(user))
        if len(user_info) != 3:
            raise Exception("Abnormal user_info in: "+ post) 
        #print('us')

        text = soup.find_all(class_="bbWrapper")
        repost_num = len(text)
        original_post = str(text[0]).replace('<br/>','').replace('</div>','').replace('<div class="bbWrapper">','')
        #print('tx')
        #print(original_post)
        return [user_info[0], user_info[1], user_info[2], repost_num, original_post, time]
    except:
        return [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]