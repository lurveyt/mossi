"""
It is intended to take HTML files from the fantasy baseball program (provided by Rich)
and combine the rosters for pitching and position players into single files.
"""

import os
import re
import urllib.request
from bs4 import BeautifulSoup

# files provided by Rich
# TODO: get 'year' out of the code
year = '2001'
print(f"Building '{year} rosters...")

roster_path = os.path.join(os.getcwd(), r"mossi_data\rosters")

def file_writer(wfile, d):
    """
    write data dictionary to wfile

    :param str wfile: file name to write into
    :param dict d: dictionary of keys
    """
    print(f"Writing: {os.path.abspath(wfile)}")
    with open(os.path.join(roster_path, wfile), 'w') as W:
        for lg, teams in sorted(d.items()):
            for team, players in sorted(teams.items()):
                for player in players:
                    W.write(f"{lg};")
                    W.write(";;".join([team, player]) + "\n")


files = []
for f in os.listdir(roster_path):
    if 'roster' in f.lower() and year in f.lower() and f.lower().endswith('html'):
        files.append(os.path.join(roster_path, f))

# establish local dictionaries for data capture
d_pitch = {}
d_pos = {}


def read_table_for_names(table, sleague, pdict):
    """
    Read the table and add extracted named to dictionary, formatted.

    :param table: the HTML soup table
    :param str sleague: league string
    :param dict pdict: the dictionary to add data to
    :return: the dictionary with added data
    :rtype: dict
    """
    for row in table.find_all('tr'):
        # keep only the lines that have text
        table_data = [s.string.strip() for s in row.find_all('td')]
        # skip blank line in table
        if not table_data[0]:
            continue
        # skip headers
        if any([k for k in ['PLAYERS', 'PITCHERS'] if k in table_data[0]]):
            continue
        # add ' to grade because MS Excel is a shit program
        table_data[2] = "'{0}".format(table_data[2].strip())
        # get the existing list
        existing = pdict[sleague].get(team_name, [])
        # update the team sub dict
        dteam = {team_name: existing + [';'.join(map(str, table_data))]}
        # update the league dict
        pdict[sleague].update(dteam)

    return pdict


for filex in files:
    # turn the html file into soup object
    url = (r"file:///" + filex).replace("\\", "/")
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')

    for node in soup.find_all("p"):
        # get the league if it's a new league
        # league or Division always starts the data segment
        if "AL " in node.text or "NL " in node.text or "Division" in node.text:
            pattern = re.compile("[AN]L")

            if pattern.search(node.text):
                league = node.text
            else:
                league = " ".join([pattern.search(string=filex).group(), node.text])

            d_pitch.update({league: {}})
            d_pos.update({league: {}})
            continue
        # get the team if its a new team,
        else:
            team_name = node.text.split(r"(")[0].strip()
            # get the next table down
            main_table = node.nextSibling.nextSibling.tr
            # the two sub tables are pitchers and postion players
            pitch_table = main_table.contents[1].contents[1]
            player_table = main_table.contents[3].contents[1]

            # read the tables for the players
            d_pitch = read_table_for_names(pitch_table, league, d_pitch)
            d_pos = read_table_for_names(player_table, league, d_pos)


# write data to files
# file_writer(wfile=f"roster_{year}_pitchers.txt", d=d_pitch)
# file_writer(wfile=f"roster_{year}_players.txt", d=d_pos)

# combine to single file
d_all = {}
for divName, divDict in d_pos.items():
    d_all.update({divName:{}})
    for teamName in divDict.keys():
        d_all[divName][teamName] = d_pos[divName][teamName] + d_pitch[divName][teamName]
file_writer(wfile=f"roster_{year}_all.txt", d=d_all)
