
import requests
from bs4 import BeautifulSoup


def asyncGet(url):
    page = requests.get(url)
    job_links = []
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        div = soup.find("div", attrs={"class": "fusion-posts-container"})
        for links in div.find_all("a"):
            job_links.append(links.get("href"))
    return job_links
