from em_driver.Database import DatabaseModel
import datetime


def connect():
    # connect to scrap database
    database = DatabaseModel("scrap")
    return database


def create_table(
    name,
):
    # create table
    connect().create_table(
        name,
        field_set=["qualification TEXT", "Timestamp Text"],
    )


def insert_qualifications_data(table, qualifications):
    #  inserting qualifications into database

    for items in qualifications:
        data = (items.replace("\n", " "), datetime.datetime.now())
        connect().insert(table, data)


def insert_url_data(table, urls):
    #  inserting scrapped url list to database


    data = (urls, datetime.datetime.now())
    connect().insert(table, data)


def get_records(table):
    # get data from given table
    data = connect().get_all_from(table)
    return data


def show_data(table):
    # display data in table
    print(connect().get_all_from(table))
