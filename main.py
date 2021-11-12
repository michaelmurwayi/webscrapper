import sys
import requests
import schedule
import time
from common import qual_insert, url_insert, create_table
from scrapper import bms, cps, jks, jws, jms


def check_host_name(url):
    # check site host name from provided url
    try:
        response = requests.get(url)
        if response.status_code == 200:
            host_name = url.split(".")[1]
            return host_name
        else:
            print("Please check provided Url")
    except Exception as e:
        raise Exception("Host seems unreachable")


def scrap_data(url):
    host_name = check_host_name(url)
    # pick which module to use based on hostname provided
    if host_name == "brightermonday":
        # brighter monday scrapper module
        data = bms(url)

        'print("no qualifications to save")' if len(
            data
        ) == 0 else "save_qualifications_to_db(url, data) ,save_urls_to_db(url, data)"

        return data

    elif host_name == "careerpointkenya":
        #  use careers point scrapper module
        data = cps(url)

        'print("no qualifications to save")' if len(
            data
        ) == 0 else "save_qualifications_to_db(url, data) ,save_urls_to_db(url, data)"

        return data

    elif host_name == "myjobmag":
        # use my job mag scrapper module
        data = jms(url)

        'print("no qualifications to save")' if len(
            data
        ) == 0 else "save_qualifications_to_db(url, data) ,save_urls_to_db(url, data)"

        return data

    elif host_name == "jobsinkenya":
        # use my job mag scrapper module
        print(f"Scrapping data from {url}")
        data = jks(url)

        if len(data) == 0:
            print("no qualifications to save")
        else:
            save_qualifications_to_db(url, data)
            # save_urls_to_db(url, data)

        return data

    elif host_name == "jobwebkenya":
        # use my job web kenya scrapper module
        print(f"Scrapping data from {url}")
        data = jws(url)

        if len(data) == 0:
            print("no qualifications to save")
        else:
            save_qualifications_to_db(url, data)
            # save_urls_to_db(url, data)

    #     return data

    else:
        print("no module yet for this website. We are working on it")
        return None


def save_qualifications_to_db(url, data):
    # save all scrapped qualifications in sqlite db

    table = url.split(".")[1]
    create_table(table)

    for items in data:
        try:
            data = items["Qualification"]
            qual_insert(table, data)
        except Exception:
            pass

    return "data inserted"


def save_urls_to_db(url, data):

    table = url.split(".")[1] + "_url"
    create_table(table)
    for items in data:
        try:
            data = items["url"]
            url_insert(table, data)
        except Exception:
            pass

    return "data inserted"


def main(url):

    host_name = check_host_name(url)
    scrap_data(url)


url_list = [
    "https://www.myjobmag.co.ke/",
    "https://www.brightermonday.co.ke/",
    "https://www.careerpointkenya.co.ke/",
    "https://www.jobsinkenya.co.ke/",
    "https://www.jobwebkenya.com/",
]

if __name__ == "__main__":
    main(url_list[1])
