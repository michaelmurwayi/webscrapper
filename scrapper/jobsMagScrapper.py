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
        link_path = soup.find_all("a", {"id": "view-all"})[2].get("href")
        ("a")
        hospitality = "/hospitality"
        url = f"{base_url}{link_path}{hospitality}"
    return url


def web_scrap_job_links(pagination_list):
    # get list of all jobs on the page
    job_links = []
    for URL in pagination_list:
        page = requests.get(URL)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            div = soup.find_all("li", {"class": "mag-b"})
            for links in div:
                job_path = str(links).split("/")[2].split(">")[0].replace('"', "")
                data = URL.split("/")
                data.pop(1)
                url = "//".join(data[:2])
                link = f"{url}/job/{job_path}"
                job_links.append(link)

    return job_links


def get_page_pagination(pagination_list):
    # get all paginated pages in hospitatlity link
    new = get_next_page(pagination_list[-1], pagination_list)
    return new


def get_next_page(URL, pagination_list):

    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            data = soup.find("ul", {"class": "setPaginate"}).text
            path_list = [int(i) for i in str(data)]
            for items in path_list:
                new_link = f"{URL}/{items}"
                pagination_list.append(new_link)
        except Exception:
            print(pagination_list)
            # web_scrap_job_links(pagination_list)
            return URL

    return pagination_list


def qualifications_scrapping(URL):

    URL = get_job_url(URL)

    pagination_links = []
    pagination_list = get_next_page(URL, pagination_links)

    # get lists of all hospitality jobs available
    job_links = web_scrap_job_links(pagination_list)

    # Get all individual links from link
    # make a request to get page data
    data = []
    for link in job_links:
        page = requests.get(link)
        print(link)
        # check url status code and proceed if code is 200 else terminate program
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            try:

                qualification_list = (
                    soup.find("ol").text.replace("\xa0", " ").split("\n")
                )
                results = {
                    "url": link,
                    "Qualification": qualification_list[1:-1],
                }
                data.append(results)
            except Exception:
                results = {"url": link, "Qualification": "Problem with this link"}
        else:
            print("something went wrong, please check provided URL")
            data = {}

    return data


# if __name__ == "__main__":
#     base_url = "https://www.myjobmag.co.ke"
