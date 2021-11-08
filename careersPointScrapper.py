import requests
from bs4 import BeautifulSoup
import json
import urllib
import re
import db
import time
# function to build URI
from _thread import start_new_thread


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


def web_scrap_job_links(pagination_list):
    print(pagination_list)
    # get list of all jobs on the page
    link_temp = pagination_list[0]

    job_links = []
    t = time.time()

    error = False
    counter = 0
    page_ = 2

    x = 1

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
        print("Job done", link)

    while not error:
        if counter == 0:
            URL = link_temp
        else:
            substr = link_temp.split("page")[0]
            URL = substr + "page" + "/" + str(page_)

        start_new_thread(worker, (URL,))
        counter += 1
        page_ += 1

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
    # import ipdb

    # ipdb.set_trace()
    t = time.time()
    page = requests.get(URL)
    print(time.time() - t)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            next_page_url = soup.find("a", attrs={"class": "pagination-next"}).get(
                "href"
            )
            pagination_list.append(next_page_url)
        except Exception:
            return pagination_list

    return pagination_list


def qualifications_scrapping(URL):
    URL = get_job_url(URL)
    pagination_links = []
    pagination_list = get_next_page(URL, pagination_links)
    print(pagination_list)
    # get lists of all hospitality jobs available
    job_links = web_scrap_job_links(pagination_list)
    # Get all individual links from link
    # make a request to get page data
    data = []
    for link in job_links:

        page = requests.get(link)

        # check url status code and proceed if code is 200 else terminate program
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            try:

                qualification_list = soup.find(
                    id="content").find_all("ul")[1].text
                results = {
                    "url": link,
                    "Qualification": qualification_list.split("\n")[1:-1],
                }
                data.append(results)
            except IndexError:
                results = {"url": link,
                           "Qualification": "Problem with this link"}
        else:
            print("something went wrong, please check provided URL")
            data = {}

    return data


# if __name__ == "__main__":
#     base_url = "https://www.careerpointkenya.co.ke"

#     data = qualifications_scrapping(URL)
