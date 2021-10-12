import requests
from bs4 import BeautifulSoup
import json
import urllib
import re

# function to build URI
def get_job_url(base_url):
    page = requests.get(base_url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        div = soup.find("div", {"id": "jobcategory"}).find_all("a")
        for index, items in enumerate(div):
            search = "Hospitality"
            data, index = re.findall(r"\b" + search + r"\b", str(items)), index
            if data:
                tag = div[index]
                url = tag.get("href")
    return url


def web_scrap_job_links(url):
    job_links = []
    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        div = soup.find("div", attrs={"class": "fusion-posts-container"})
        for links in div.find_all("a"):
            job_links.append(links.get("href"))
    return job_links


def qualifications_scrapping(URL):
    # get lists of all hospitality jobs available
    job_links = web_scrap_job_links(URL)
    # Get all individual links from link
    # make a request to get page data
    data = []
    for link in job_links:
        page = requests.get(link)

        # check url status code and proceed if code is 200 else terminate program
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            try:
                qualification_list = soup.find(id="content").find_all("ul")[1].text
                results = {
                    "url": link,
                    "Qualification": qualification_list.split("\n")[1:-1],
                }
                data.append(results)
            except IndexError:
                results = {"url": link, "Qualification": "Problem with this link"}
        else:
            print("something went wrong, please check provided URL")
    print(data)


if __name__ == "__main__":
    base_url = "https://www.careerpointkenya.co.ke"
    URL = get_job_url(base_url)
    qualifications_scrapping(URL)
