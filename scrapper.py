import requests 
from bs4 import BeautifulSoup
import json

# Get the page url 
URL = "https://www.careerpointkenya.co.ke/2021/09/aurum-consultants-school-cateress-job/"

# make a request to get page data 
page = requests.get(URL)

# check url status code and proceed if code is 200 else terminate program
if page.status_code == 200:
    soup = BeautifulSoup(page.content, "html.parser")
    qualification_list = soup.find(id="content").find_all("ul")[1].text
    print(qualification_list)
else:
    print("something went wrong, please check provided URL")