from ..common import get_records

"""
This Module takes table name
Reads data from sqlite
Produces a dataset for all stored data
"""

table = "brightermonday"


def load_data(table):
    data = get_records(table)
    for index, items in enumerate(data):
        if len(items) <= 1:
            data.pop(index)

    return data
