import sys

sys.path.append("..")
from common import get_records

"""
This Module takes table name
Reads data from sqlite
Produces a dataset for all stored data
"""


table = "brightermonday"

tables = ["brightermonday", "careerpointkenya", "jobwebkenya"]


def load_single_table_data(table):
    # read data from single table in the database

    data_set = []
    data = get_records(table)
    for index, items in enumerate(data):
        if len(items[0]) > 1:
            data_set.append(items[0])

    return data_set


def load_all_table_data(tables):
    # Takes list of tables and returns data_set of all i

    data_sets = []
    for table in tables:
        data = load_single_table_data(table)
        data_sets.append(data)

    data_set = [ qualification for data in data_sets for qualification in data]

    return data_set


# load_single_table_data(table)

load_all_table_data(tables)
