from bs4 import BeautifulSoup
import requests

from common.common import prt_dev


def cps_worker(link):
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
            prt_dev("Job complete", link)
            return results
        except IndexError:
            prt_dev("Job complete", link)
            results = {"url": link,
                       "Qualification": "Problem with this link"}
            return results
