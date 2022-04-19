""",
It is intended to take HTML files from the fantasy baseball program (provided by Rich)
and combine the rosters for pitching and position players into single files.
"""

import os
import re
import urllib.request
from bs4 import BeautifulSoup

# files provided by Rich
# TODO: get 'year' out of the code
year = '83'
roster_path = os.path.join(os.getcwd(), r"mossi_data\rosters")


def file_writer(wfile, d):
    """write data dictionary to wfile
    :param wfile: file name to write into
    :type wfile: str
    :param d: dictionary of keys
    :type d: dict
    """
    with open(os.path.join(roster_path, wfile), 'w') as W:
        for league, teams in sorted(d.items()):
            for team, players in sorted(teams.items()):
                for player in players:
                    W.write(f"{league};")
                    W.write(";;".join([team, player]) + "\n")


files = []
for f in os.listdir(roster_path):
    if 'roster' in f.lower() and year in f.lower() and f.lower().endswith('html'):
        files.append(os.path.join(roster_path, f))

# establish local dictionaries for data capture
d_pitch = {}
d_pos = {}


def read_table_for_names(table, league, pdict):
    """
    Read the table and add extracted named to dictionary, formatted.

    :param table: the HTML soup table
    :param league: league string
    :param pdict: the dictionary to add data to
    :return: the dictionary with added data
    """
    for row in table.find_all('tr'):
        # keep only the lines that have text
        table_data = [s.string.strip() for s in row.find_all('td')]
        # skip blank line in table
        if not table_data[0]:
            continue
        # add ' to grade because MS Excel is a shit program
        table_data[2] = "'{0}".format(table_data[2].strip())
        # get the existing list
        existing = pdict[league].get(team_name, [])
        # update the team sub dict
        dteam = {team_name: existing + [';'.join(map(str, table_data))]}
        # update the league dict
        pdict[league].update(dteam)

    return pdict


for filex in files:
    # turn the html file into soup object
    url = (r"file:///" + filex).replace("\\", "/")
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')

    for node in soup.find_all("p"):
        # get the league if it's a new league
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
file_writer(wfile="roster_{}_pitchers.txt".format(year), d=d_pitch)
file_writer(wfile="roster_{}_players.txt".format(year), d=d_pos)
