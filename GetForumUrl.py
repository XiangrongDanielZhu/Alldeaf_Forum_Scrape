import requests
from bs4 import BeautifulSoup
import re

url = "https://www.alldeaf.com/"

def GetForumUrl(url):
    # Use try-except to see if the files are successully written locally
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        # All forum links are recorded in "node-title class"
        links = soup.find_all(class_="node-title")

        link = []
        for item in links:
            link.append(url + re.compile(r'.*href="/(.*?)/"').findall(str(item))[0])

        # Write results into txt file
        with open("forums_url.txt","w") as f:
            for item in link:
                f.writelines(item+'\n')

    except:
        return False
        
    return True

    