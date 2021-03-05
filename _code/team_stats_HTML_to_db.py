#!/usr/env/bin python
"""
This code was written by Tim Lurvey C 2021
Process the stats html files from Mossi league
"""

import os
import copy
import urllib.request
from bs4 import BeautifulSoup

# project files
from _code.utils.utilities import configure_logger
from db.models import *

# LEVEL = os.environ.get('DEBUG_LEVEL','DEBUG')
LEVEL = 'INFO'
log = configure_logger(name=__name__,
                       console_level=LEVEL,
                       log_file="{}.log".format(__file__))


def get_all_files(stat_path):
    """
    Search a path and find all matching files for stat import.

    :param stat_path: the path to find all new stat files
    :type stat_path: str
    :return: list
    """
    files = []
    for filex in os.listdir(path=stat_path):
        if filex.endswith(".html"):
            files.append(filex)
            log.debug(f"Found file: {filex}")
    log.debug(f"Found {len(files)} in {stat_path}")
    return files

def formatter(value):
    """
    Attempt to convert a value to a float or int.
    If not a float of int, return as str.
    :param value: value to convert
    :type value: str
    :retrun: converted value
    :rtype: str, float, int
    """
    if "." in value:
        try:
            return float(value)
        except ValueError:
            return value
    else:
        try:
            return int(value)
        except ValueError:
            return value

def get_pitching(soup):
    data = {}
    pass

def get_batting(soup):
    """
    mine batting player html and build dictionary
    :param soup: soup
    :return: dict
    """
    # get heading attributes
    year, team, xtype = map(str.strip, soup.title.contents[0].split("-"))
    log.debug(f"Working on {year} {team} {xtype}")
    players = {}

    # build dictionary keys
    player = {
        "name": "",
        "master_team": team,
        "year": int(year)
    }

    second = False
    # for each table, get the keys and player values
    tables = soup.body.find_all("table")
    for table in tables:
        keys = []
        # 'tr' is a tablerow identifier in html
        rows = table.find_all("tr")
        for row in rows:
            # if the row is not blank, proceed
            if row.text.strip():
                # new placeholder dictionary with default values
                playerx = copy.deepcopy(player)
                # only the headings are underlined, find we .u
                if row.u:
                    # get table keys, replace any bad characters in the keys
                    keys += map( lambda s: s
                                 .replace('/', '_')
                                 .replace('2B', 'DBL')
                                 .replace('3B', 'TPL'),
                                    row.text.strip().split("\n"))
                    log.debug(f"Found keys: {keys}")
                    # override first key as 'name'
                    keys[0] = "name"
                # anything not underlined is a player stat to be logged
                else:
                    # get the values in the row
                    vals = row.text.strip().split("\n")
                    log.debug(f"Found vals: {vals}")
                    # pull name
                    name = vals[0]
                    # apply formatter to all values
                    new_vals = map(formatter, vals)
                    # apply key, value pairs to a new dictionary
                    kv_dict = dict(zip(keys, new_vals))
                    # put them into the playerx dictionary
                    playerx.update(kv_dict)
                    # pull any previous values into the playerx dictionary
                    playerx.update(players.get(name, {}))
                    # put the whole playerx dictionary into the players dictionary
                    players.update({playerx.get('name'): playerx})
                    log.info(f"Player logged {name}. {rows.index(row)} of {len(rows)-1}")

    return players

def get_HTML_data(html_path):
    """
    Use Beautiful soup to mine the data.  Find the type of data to mine and
    pass the soup object to the appropriate method.

    :param html_path: the html path found
    :type html_path: str
    :return: dict
    """

    methods = {
        "Batting": get_batting,
        "Pitching": get_pitching
    }

    # turn the html file into soup object
    url = (r"file:///" + html_path).replace("\\", "/")
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')

    method = soup.title.contents[0].split("-")[-1].strip().split(" ")[-1]

    log.debug(f"Running {method} on {html_path}")
    return methods.get(method)(soup)

def save_to_db(data):
    """
    save each players statline to the database
    :param data: data line of the player
    :type data: dict
    :return: None
    """
    pass


if __name__ == '__main__':
    log.debug(f"\n\nRun program {__file__}")
    TEST_PATH = r"..\mossi_stat"

    new_files = get_all_files(TEST_PATH)

    for f in new_files:
        data = get_HTML_data(os.path.join(TEST_PATH, f))
        for k, v in data.items():
            save_to_db(v)