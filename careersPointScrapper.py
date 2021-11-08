import requests
from bs4 import BeautifulSoup
import json
import urllib
import re
from common import prt_dev
from common import cps_worker
from common.common import Colors
import db
import time
# function to build URI
from _thread import start_new_thread

import concurrent.futures


def get_job_url(base_url):
    # scrap hospitality link from home page job category
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


def web_scrap_job_links(pagination_link):
    # get list of all jobs on the page
    link_temp = pagination_link

    job_links = []

    error = False
    counter = 0
    page_ = 2
    complete = []

    # mini workers for link extraction
    def worker(link):
        global error
        global counter
        page = requests.get(link)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            div = soup.find("div", attrs={"class": "fusion-posts-container"})
            for links in div.find_all("a"):
                job_links.append(links.get("href"))
        elif page.status_code == 404:
            error = True
        complete.append(link)

    while not error and counter < 500:
        if counter == 0:
            URL = link_temp
        else:
            substr = link_temp.split("page")[0]
            URL = substr + "page" + "/" + str(page_)

        start_new_thread(worker, (URL,))
        counter += 1
        page_ += 1

    # await threads to finish
    while len(complete) < 101:
        pass

    return job_links


def get_next_page(URL):
    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            next_page_url = soup.find("a", attrs={"class": "pagination-next"}).get(
                "href"
            )
            return next_page_url
        except:
            raise Exception("No next page")


def qualifications_scrapping(URL):

    prt_dev("Staring jobs...", f"{Colors.OKGREEN}INFO")
    t = time.time()
    URL = get_job_url(URL)

    pagination_link = get_next_page(URL)
    job_links = web_scrap_job_links(pagination_link)

    data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(job_links)) as executor:
        worker_results = executor.map(cps_worker, job_links)
        for result in worker_results:
            data.append(result)
    prt_dev(time.time() - t, "seconds")
    return data
