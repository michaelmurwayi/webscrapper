import sys
import requests
import db
from brightMondayScrapper import qualifications_scrapping
import careersPointScrapper
import jobsMagScrapper


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
        data = qualifications_scrapping(url)
        # save_to_db(url, data)
        return data

    elif host_name == "careerpointkenya":
        #  use careers point scrapper module
        data = careersPointScrapper.qualifications_scrapping(url)
        # save_to_db(url, data)

        return data

    # elif host_name == "myjobmag":
    #     # use my job mag scrapper module
    #     data = jobsMagScrapper.qualifications_scrapping(url)
    #     save_to_db(url, data)

    #     return data

    else:
        print("no module yet for this website. We are working on it")
        return None


def save_to_db(url, data):
    table = url.split(".")[1]
    db.create_table(table)
    for items in data:
        data = items["Qualification"]
        db.insert_data(table, data)
    db.show_data(table)

    return "data inserted"


def main():
    url = get_input()
    check_host_name(url)
    qualifications = scrap_data(url)


if __name__ == "__main__":
    main()
