""",
It is intended to take HTML files from the fantasy baseball program (provided by Rich)
and combine the rosters for pitching and position players into single files.
"""

import os
import urllib.request
from bs4 import BeautifulSoup

def file_writer(wfile, d):
    """write data dictionary to wfile
    :param wfile: file name to write into
    :type wfile: str
    :param d: dictionary of keys
    :type d: dict
    """
    with open(wfile, 'w') as W:
        for k in sorted(d.keys()):  # for each team
            for val in d.get(k):    # for each player
                W.write(';;'.join([k, val]) + "\n")


# files provided by Rich
year = '75'
my_path = r"C:\Users\pants\PycharmProjects\FantasySports"

files = []
for f in os.listdir(my_path):
    if 'roster' in f.lower() and year in f.lower() and f.lower().endswith('html'):
        files.append(os.path.abspath(f))

# global dictionaries
d_pitch_all = {}
d_pos_all = {}

for filex in files:
    # turn the html file into soup object
    url = (r"file:///" + filex).replace("\\", "/")
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')
    # establish local dictionaries for data capture
    d_pitch = {}
    d_pos = {}
    # loop by team
    for team in soup.body.find_all("p"):
        # data capture setup
        team_name = team.text.split("(")[0].strip()
        d_pitch.update({team_name: []})
        d_pos.update({team_name: []})
        tables = [t for t in team.parent.find_all("td") if not t.attrs]
        # loop over all sub-tables
        for i in range(0, len(tables)+1):
            # each team has 2 tables, one pitching and one position player
            # only parse 2 tables per team name
            if (i - i % 2)/2 == (len(d_pitch) - 1):
                # consume table chunk-wise by 6
                for multiple in range(0, int((len(tables[i].find_all("td"))/6))-1):
                    table_data = []
                    for n in range(0, 6):
                        table_data.append(tables[i].find_all("td")[n + (multiple * 6)].string)

                    # add ' to grade because MS Excel is a shit program
                    table_data[2] = "'{0}".format(table_data[2].strip())

                    # add data to dictionary
                    if "pitchers" in tables[i].find_all("td")[0].string.lower():
                        # keep only player lines, not headers
                        if 'PITCHERS' not in table_data[0]:
                            d_pitch.update({team_name: d_pitch.get(team_name) + [';'.join(map(str, table_data))]})
                    else:
                        if 'PLAYERS' not in table_data[0]:
                            d_pos.update({team_name: d_pos.get(team_name) + [';'.join(map(str, table_data))]})
    # push the local dict to the global
    d_pitch_all.update(d_pitch)
    d_pos_all.update(d_pos)

# write data to files
file_writer(wfile="roster_{}_pitchers.txt".format(year), d=d_pitch_all)
file_writer(wfile="roster_{}_players.txt".format(year), d=d_pos_all)
