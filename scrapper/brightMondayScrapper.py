import requests
from bs4 import BeautifulSoup
import json
import urllib
import re
from common import workers
import time
import concurrent.futures
from _thread import start_new_thread
from common import bms_worker

# function to build URI


def get_job_url(base_url):
    # scrap hospitality link from home page job category
    page = requests.get(base_url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        div = soup.find("section", {"id": "jobs-by-job-function"}).find_all("a")
        for index, items in enumerate(div):
            search = "Hospitality"
            data, index = re.findall(r"\b" + search + r"\b", str(items)), index
            if data:
                tag = div[index]
                url = tag.get("href")
    return url


def web_scrap_job_links(pagination_list):
    # get list of all jobs on the page
    job_links = []

    if isinstance(pagination_list, str):
        page = requests.get(pagination_list)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            div = soup.find("div", attrs={"class": "search-main__content"}).find_all(
                "a"
            )
            div.pop(0)

            for links in div:
                job_links.append(links.get("href"))
    else:
        t = time.time()
        for URL in pagination_list:
            page = requests.get(URL)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
                div = soup.find("div", attrs={"class": "fusion-posts-container"})
                for links in div.find_all("a"):

                    job_links.append(links.get("href"))
                    # print(job_links)
        print(time.time() - t)
    return job_links


def get_page_pagination(pagination_list):
    # get all paginated pages in hospitatlity link
    new = get_next_page(pagination_list[-1], pagination_list)
    return "done"


def get_next_page(URL, pagination_list):

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


def qualifications_scrapping(base_url):
    URL = get_job_url(base_url)
    pagination_links = []
    pagination_list = get_next_page(URL, pagination_links)
    # get lists of all hospitality jobs available
    job_links = web_scrap_job_links(pagination_list)
    filtered_links = [link for link in job_links if link.startswith("https://")]
    # Get all individual links from link
    # make a request to get page data

    data = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(filtered_links)
    ) as executor:
        workers_result = executor.map(bms_worker, filtered_links)

        for results in workers_result:
            data.append(results)

    return data
