import sys
import requests
import schedule
import time
import db
import brighterMondayScrapper
import careersPointScrapper
import jobsMagScrapper
import jobInKenya
import jobWebScrapper


def get_input():
    # get input from the terminal, input is passed during script running

    url = sys.argv[1]
    return url


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
        data = brighterMondayScrapper.qualifications_scrapping(url)

        if len(data) == 0:
            print("no qualifications to save")
        else:
            save_qualifications_to_db(url, data)
            save_urls_to_db(url, data)

        return data

    elif host_name == "careerpointkenya":
        #  use careers point scrapper module
        data = careersPointScrapper.qualifications_scrapping(url)

        if len(data) == 0:
            print("no qualifications to save")
        else:
            save_qualifications_to_db(url, data)
            save_urls_to_db(url, data)

        return data

    elif host_name == "myjobmag":
        # use my job mag scrapper module
        data = jobsMagScrapper.qualifications_scrapping(url)

        if len(data) == 0:
            print("no qualifications to save")
        else:
            save_qualifications_to_db(url, data)
            save_urls_to_db(url, data)

        return data

    elif host_name == "jobsinkenya":
        # use my job mag scrapper module
        print(f"Scrapping data from {url}")
        data = jobInKenya.qualifications_scrapping(url)

        if len(data) == 0:
            print("no qualifications to save")
        else:
            save_qualifications_to_db(url, data)
            save_urls_to_db(url, data)

        return data

    elif host_name == "jobwebkenya":
        # use my job web kenya scrapper module
        print(f"Scrapping data from {url}")
        data = jobWebScrapper.qualifications_scrapping(url)

        if len(data) == 0:
            print("no qualifications to save")
        else:
            save_qualifications_to_db(url, data)
            save_urls_to_db(url, data)

        return data

    else:
        print("no module yet for this website. We are working on it")
        return None


def save_qualifications_to_db(url, data):
    # save all scrapped qualifications in sqlite db

    table = url.split(".")[1]
    db.create_table(table)
    for items in data:
        data = items["Qualification"]
        db.insert_qualifications_data(table, data)

    return "data inserted"


def save_urls_to_db(url, data):

    table = url.split(".")[1] + "_url"
    db.create_table(table)
    for items in data:
        data = items["url"]
        db.insert_url_data(table, data)

    return "data inserted"


def main(url):

    host_name = check_host_name(url)
    qualifications = scrap_data(url)


url_list = [
    "https://www.myjobmag.co.ke/",
    "https://www.brightermonday.co.ke/",
    "https://www.careerpointkenya.co.ke/",
    "https://www.jobsinkenya.co.ke/",
    "https://www.jobwebkenya.com/",
]


schedule.every().day.at("07:30").do(main(url_list[0]))
schedule.every().day.at("08:00").do(main(url_list[1]))
schedule.every().day.at("08:30").do(main(url_list[2]))
schedule.every().day.at("09:00").do(main(url_list[3]))
schedule.every().day.at("09:30").do(main(url_list[4]))
