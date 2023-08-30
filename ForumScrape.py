import requests
from bs4 import BeautifulSoup
import re
from GetForumUrl import GetForumUrl
from GetPage import GetPage
from GetPost import GetPost
import pandas as pd
import numpy as np

#url = "https://www.alldeaf.com/"
#GetForumUrl(url)

url = "https://www.alldeaf.com/"
with open("forums_url.txt","r") as f:
    links = f.readlines()
#print(len(links))


link = "https://www.alldeaf.com/forums/deaf-products-technologies.9/"
file_path = re.compile(r'.*forums/(.*?)/').findall(link)[0] + '.csv'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
}
r = requests.get(link,headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')
forum_post = soup.find_all(class_="structItem-title")
print(forum_post)

post_link = []
post_title = []
User_registration_time = []
Messages = []
Reaction_score = []
Number_of_repost = []
Text = []
Publish_time = []

page = GetPage(link)
print(page)


for PageNum in range(2,page+1):
    try:
        page_link = link + 'page-'+str(PageNum)

        headers = {
        'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
        }

        r = requests.get(page_link,headers=headers, timeout=20)
        soup = BeautifulSoup(r.content, 'html.parser')
        forum_post = soup.find_all(class_="structItem-title")
        for item in forum_post:
            #post_link.append(re.compile(r'.*href="/(.*?)/"').findall(str(item))[0])
            posttitle = re.compile(r'.*">(.*?)</a').findall(str(item))
            postlink = re.compile(r'.*href="/(.*?)/"').findall(str(item))
            if postlink == []:
                post_link.append(np.nan)
            else:
                post_link.append(url+postlink[0])
            if posttitle == []:
                post_title.append(np.nan)
            else:
                post_title.append(posttitle[0])
            #post_title.append(re.compile(r'.*">(.*?)</a').findall(str(item))[0])
        print('T:finished ' + str(PageNum) + ' page.')
        print(len(post_link)==len(post_title))    
    except:
        print('F:unable to scrape ' + str(PageNum) + ' page')

for posts in post_link:
    info = GetPost(posts)
    print('Success: '+ posts)
    User_registration_time.append(info[0])
    Messages.append(info[1])
    Reaction_score.append(info[2])
    Number_of_repost.append(info[3])
    Text.append(info[4])
    Publish_time.append(info[5])
    length = len(User_registration_time)
    if len(Messages)==length and len(Reaction_score)==length and len(Number_of_repost)==length and len(Text)==length and len(Publish_time)==length:
        print(True)
    else:
        raise Exception("Wrong Length in "+ posts)

data = pd.DataFrame({
            'Title': post_title,
            'Link': post_link,
            'Time': Publish_time,
            'Reposts': Number_of_repost,
            'User Registration': User_registration_time,
            'User Reaction Score': Reaction_score,
            'User Messages': Messages,
            'Content': Text })


data.to_csv(file_path,sep=',',index=False,header=True)
print(data)

