from bs4 import BeautifulSoup
import requests

from common.common import prt_dev


def cps_worker(link):
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
            prt_dev("Job complete", link)
            return results
        except IndexError:
            prt_dev("Job complete", link)
            results = {"url": link, "Qualification": "Problem with this link"}


def bms_worker(link):
    page = requests.get(link)

    # check url status code and proceed if code is 200 else terminate program
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        try:

            qualification_list = (
                soup.find("div", "description-content__content").find("ul").text
            )

            results = {
                "url": link,
                "Qualification": qualification_list.split(","),
            }
            prt_dev("Job Complete", link)
            return results
        except Exception:
            results = {"url": link, "Qualification": "Problem with this link"}
    else:
        prt_dev("something went wrong, please check provided URL", link)


def jws_worker(link):
    page = requests.get(link)
    # make a request to get page data

    # check url status code and proceed if code is 200 else terminate program
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        try:

            qualification_list = [
                items.text
                for items in soup.find("div", {"class": "job-details"}).find_all("li")
            ]

            results = {
                "url": link,
                "Qualification": qualification_list,
            }
            prt_dev("Job Complete", link)
            return results
        except Exception:
            results = {"url": link, "Qualification": "Problem with this link"}
    else:
        prt_dev("something went wrong, please check provided URL", link)


def jks_worker(link):
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
            prt_dev("Job Complete", link)
            return results
        except IndexError:
            results = {"url": link, "Qualification": "Problem with this link"}
    else:
        print("something went wrong, please check provided URL")
        data = {}
