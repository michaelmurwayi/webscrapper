import requests
from bs4 import BeautifulSoup
import json
import urllib
import re

# function to build URI
def get_job_url(base_url):
    # scrap hospitality link from home page job category
    page = requests.get(base_url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        div = soup.find("ul", {"class": "dcw"}).find("li", {"class": "cat-item-27"})
        url = (
            str(div)
            .replace('<li class="cat-item cat-item-27"><a href="', "")
            .split('">')[0]
        )

    return url


def web_scrap_job_links(pagination_list):
    # get list of all jobs on the page
    job_links = []

    if isinstance(pagination_list, str):
        page = requests.get(pagination_list)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            div = soup.find("article", attrs={"class": "blog-view"}).find_all("a")
            div.pop(0)

            for data in div:

                try:
                    link = (
                        re.search("%s(.*)%s" % ('"', '"'), str(data))
                        .group(1)
                        .split('href="')[1]
                    )
                    job_links.append(link)
                except IndexError:
                    return job_links
            print(job_links)
    else:
        for URL in pagination_list:
            page = requests.get(URL)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                div = soup.find("div", attrs={"class": "fusion-posts-container"})
            for data in div:
                link = (
                    re.search("%s(.*)%s" % ('"', '"'), str(data))
                    .group(1)
                    .split('href="')[1]
                )
                job_links.append(link)
    return job_links


def get_page_pagination(pagination_list):
    # get all paginated pages in hospitatlity link
    new = get_next_page(pagination_list[-1], pagination_list)
    return "done"


def get_next_page(URL, pagination_list):
    # get next page in pagination list
    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            next_page_url = soup.find("a", attrs={"class": "pagination-next"}).get(
                "href"
            )
            pagination_list.append(next_page_url)
            get_page_pagination(pagination_list)
        except Exception:
            # print(pagination_list)
            # web_scrap_job_links(pagination_list)
            return URL

    return pagination_list


def check_if_link_already_scrapped(url, table):
    # check if link about to scan is already in db
    # ignore link if in database
    # scrapp link if not in database
    stored_links = db.get_records(table)
    if stored_links:
        for items in stored_links:
            if url in items:
                return True
            else:
                return False
    else:
        return False


def qualifications_scrapping(base_url):
    # table for storage of scrapped links
    table = base_url.split(".")[1] + "_url"

    URL = get_job_url(base_url)

    pagination_links = []
    pagination_list = get_next_page(URL, pagination_links)
    # get lists of all hospitality jobs available

    job_links = web_scrap_job_links(pagination_list)

    # Get all individual links from link
    # make a request to get page data
    data = []
    for link in job_links:
        if check_if_link_already_scrapped(link, table):
            print("qualifications already scrapped from link")
        else:
            print(f"scrapping data from {link}")
            page = requests.get(link)

            # check url status code and proceed if code is 200 else terminate program
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                try:

                    qualification_list = (
                        soup.find("div", {"class": "entry-content"})
                        .find_all("ul")[1]
                        .text.split("\n")[1:-1]
                    )
                    results = {
                        "url": link,
                        "Qualification": qualification_list,
                    }
                    data.append(results)
                except IndexError:
                    results = {"url": link, "Qualification": "Problem with this link"}
            else:
                print("something went wrong, please check provided URL")
                data = {}

    return data
