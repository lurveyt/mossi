#!/usr/bin/env python
__author__ = 'Timothy Lurvey'

import sys
import shutil
import openpyxl
import openpyxl.utils
import numpy as np


def build_roster_dict(ids: tuple, teams: tuple):
    """ {Player_ID: Team Name}"""
    try:
        assert len(ids) == len(teams)
    except AssertionError:
        print("ID and TEAMS are different sizes!")
    #
    d = {}
    for i in range(len(ids)):
        d.update({ids[i].value: teams[i].value})
    return d


def populate_players(wb: openpyxl.workbook, roster: dict, bat_or_pit: str = 'batting'):
    """Using a roster dictionary and the year, populate the roster for current and future years"""
    # get variables
    xyear = wb['DRAFT_STATS']['C3'].value
    sheet = wb['WAR_{}'.format(bat_or_pit)]
    col = openpyxl.utils.get_column_letter([x.value for x in sheet['A1:AZ1'][0]].index('ROSTER') + 1)
    # get arrays from worksheet column data
    plyr = np.array([x[0].value for x in sheet['A2:A{}'.format(sheet.max_row)]])
    year = np.array([x[0].value for x in sheet['E2:E{}'.format(sheet.max_row)]])
    # find matches
    match_name = np.in1d(plyr, np.array(list(roster.keys())))
    match_year = year >= xyear
    match_indx = np.nonzero(match_name * match_year)[0]
    # populate team names for matches
    for i, x in enumerate(match_year):
        if x:
            val = ""
            if i in match_indx:
                val += roster.get(sheet['A{}'.format(i + 2)].value)
            sheet['{c}{r}'.format(c=col, r=i + 2)].value = val

    # for i in match_indx + 2:  # adjust for cells starting with 1
    #     sheet['{c}{r}'.format(c=col, r=i)].value = roster.get(sheet['A{}'.format(i)].value)


def main(*args):
    excel_file = r"..\MILWAUKEE_FULL_STATS2.xlsx"
    shutil.copy(src=excel_file, dst=excel_file + "_bak")
    print('opening workbook for reading...')
    r_wb = openpyxl.load_workbook(excel_file, data_only=True)
    print('- begin read')
    #
    rost_dict = build_roster_dict(teams=r_wb['ROSTERS']['A:A'], ids=r_wb['ROSTERS']['B:B'])
    print('- rosters built')
    r_wb.close()
    print('closing workbook for reading')
    #
    print('opening workbook for writing')
    w_wb = openpyxl.load_workbook(excel_file, data_only=False)
    print('- begin write')
    populate_players(wb=w_wb, roster=rost_dict, bat_or_pit='batting')
    print('- batters populated')
    #
    populate_players(wb=w_wb, roster=rost_dict, bat_or_pit='pitching')
    print('- pitchers populated')
    #
    print('saving...')
    w_wb.save(excel_file)
    print('done!')
    pass


if __name__ == '__main__':
    main(sys.argv[1:])
