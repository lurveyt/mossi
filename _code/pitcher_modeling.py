#!/usr/env/bin python
""" Documentation for {file}

Predicting pitcher ratings with ML

1.6.5
https://scikit-learn.org/stable/modules/neighbors.html#nearest-centroid-classifier
>>> from sklearn.neighbors import NearestCentroid
>>> import numpy as np
>>> X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
>>> y = np.array([1, 1, 1, 2, 2, 2])
>>> clf = NearestCentroid()
>>> clf.fit(X, y)
NearestCentroid()
>>> print(clf.predict([[-0.8, -1]]))
[1]

1.10
https://scikit-learn.org/stable/modules/tree.html#classification
>>> from sklearn import tree
>>> X = [[0, 0], [1, 1]]
>>> Y = [0, 1]
>>> clf = tree.DecisionTreeClassifier()
>>> clf = clf.fit(X, Y)
>>> clf.predict([[2., 2.]])
array([1])

""".format(file=__file__)

import os
import pandas as pd
import openpyxl
import openpyxl.utils
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from sklearn.neighbors import NearestCentroid
import numpy as np


from _code.utils.utilities import configure_logger

log = configure_logger(name=__name__,
                       console_level=20,    # INFO
                       log_file="{}.log".format(__file__))

fs = os.path.abspath(r"C:\Users\pants\PycharmProjects\FantasySports")


def pitcher_grade(path: str) -> pd.DataFrame:
    """
    Read roster data for name, grade, control.

    Process:
    ---------------
    - walk the directory
    - for each file
      - drop columns not needed
      - assign type to columns
      - split grade between 'starting' and 'relief'
      - split name to 'first_name' and 'last_name'
      - append to master DataFrame
    - return Dataframe

    :param str path: directory to walk for '*pitch*txt'
    :return: The modified dataframe
    :rtype pd.Dataframe
    """
    dftypes = {
        'team': 'string',
        'blank': 'object',
        'name': 'string',
        'th': 'string',
        'grade': 'float64',
        'relief': 'float64',
        'ctrl': 'string',
        'junk': 'object',
        'last_name': 'string',
        'first_name': 'string',
    }
    drop_keys = ['division', 'team', 'blank', 'junk', ]

    main_df = pd.DataFrame()
    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            if 'pitch' in f.lower() and f.endswith('txt'):
                log.debug(f"Reading: {f}")
                yr = int(f.split('_')[1])
                dtypes = {}
                if yr >= 77:
                    dtypes.update({'division': 'string'})
                [dtypes.update({k: v}) for k, v in dftypes.items()]
                # read the raw data
                df = pd.read_csv(os.path.join(root, f), sep=';', names=dtypes.keys())
                for dk in drop_keys:
                    if dk in df.columns:
                        df.drop([dk], axis=1, inplace=True)
                # drop header rows
                df.drop(df[df['grade'].str.contains('Grade')].index, inplace=True)
                # fix format, then split starter and relief grades
                df['grade'] = df['grade'].str.replace("'", "")
                df[['grade', 'relief']] = df['grade'].str.split('/', expand=True)
                # split the name column
                df[['last_name', 'first_name']] = df['name'].str.split(',', expand=True)
                # make the names lowercase
                df['last_name'] = df['last_name'].str.lower()
                df['last_name'] = df['last_name'].str.strip()
                df['first_name'] = df['first_name'].str.lower()
                df['first_name'] = df['first_name'].str.strip()
                df['name'] = df['name'].str.lower()
                df['name'] = df['name'].str.strip()
                # convert types
                for k in df.columns:
                    df[k] = df[k].astype(dftypes[k])
                # add year column
                df.insert(loc=1, column='year', value=1900+yr)
                # add to master dataframe
                main_df = pd.concat([main_df, df], ignore_index=True)

    # drop extra data
    main_df.drop(
        labels=['th', 'last_name', 'first_name'],
        axis=1,
        inplace=True
    )

    # # this list of the name is the second person, so their name will get + '2'
    # # update the NAME_LOOKUP.csv accordingly
    # names = {
    #     "GIBSON, Bob": (1983, 1987),
    #     "O'DONOGHUE, John": (1993, 1993),
    #     "SADOWSKI, Bob": (1963, 1966),
    #     "MILLER, Bob": (1957, 1974),
    #     "BORBON, Pedro": (1992, 2003),
    #     "SANTIAGO, Jose": (1963, 1970),
    #     "HUNTER, Jim": (1991, 1991),
    #     "ANDERSON, Rick": (1986, 1988),
    #     # "": (),
    # }
    # for name, years in names.items():
    #     main_df.loc[(main_df['name'] == name.lower()) & (main_df['year'].ge(years[0])) & (main_df['year'].le(years[-1])), 'name'] = name.lower() + "2"

    # format data columns
    int_cols = ['grade', 'relief']
    for col in int_cols:
        main_df[col] = main_df[col].fillna(0).astype('int64')

    return main_df

def pitcher_names(csv: str) -> pd.DataFrame:
    """
    Read the csv of pitcher names and playerIDs.
    Replace the existing 'name' with 'LAST, first' data and change names to lower.

    :param str csv: the csv file
    :return: pd.DataFrame
    """
    log.debug(f"Reading: {csv}")
    df = pd.read_csv(csv)
    df.rename({'name': 'name_FL'}, axis='columns', inplace=True)
    df.rename({'LAST, First': 'name'}, axis='columns', inplace=True)
    df['name'] = df['name'].str.strip()
    df['name'] = df['name'].str.lower()

    return df

def pitcher_war(csv: str) -> pd.DataFrame:
    """
    Read for all pitcher data from WAR data.  Rename and massage data for usage.

    :param str csv: the csv file
    :return: the WAR dataframe
    :rtype: pd.DataFrame
    """
    log.debug(f"Reading: {csv}")
    df = pd.read_csv(csv)
    # rename the year_ID to year
    df.rename({'year_ID': 'year'}, axis='columns', inplace=True)
    df.rename({'player_ID': 'playerID'}, axis='columns', inplace=True)

    # drop numeric columns not relevant for analysis
    df.drop(
        columns=[
            'mlb_ID',
            'salary',
            'age',
        ],
        axis='columns',
        inplace=True,
    )

    return df


def pitcher_stats(csv: str):
    """
    Get a list of pitching stats.  Do not include any traded years.

    :param str csv: csv file name
    :return: pd.DataFrame
    """
    log.debug(f"Reading: {csv}")
    df = pd.read_csv(csv)
    # convert column names for merging
    df.rename({'yearID': 'year'}, axis='columns', inplace=True)
    df.rename({'teamID': 'team_ID'}, axis='columns', inplace=True)
    df.rename({'stint': 'stint_ID'}, axis='columns', inplace=True)
    return df


def nc_classify(df: pd.DataFrame):
    """
    https://scikit-learn.org/stable/modules/neighbors.html#nearest-centroid-classifier

    >>> from sklearn.neighbors import NearestCentroid
    >>> import numpy as np
    >>> X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    >>> y = np.array([1, 1, 1, 2, 2, 2])
    >>> clf = NearestCentroid()
    >>> clf.fit(X, y)
    NearestCentroid()
    >>> print(clf.predict([[-0.8, -1]]))
    [1]

    :param pd.Dataframe df:
    :return:
    """
    log.debug('begin nearest centroid classify')

    answer_col = [
        'grade',
        # 'relief',
    ]

    input_cols = [
        'IPouts_start',
        'G',
        'GS',
        'RA',
        'xRA',
        'xRA_final',
        'runs_above_rep',
    ]

    # drop anything with NaN in estimator fields
    for c in input_cols + answer_col:
        df = df.loc[~df[c].isna()]

    # classify
    clf = NearestCentroid()
    clf.fit(X=df[input_cols],
            y=df[answer_col])

    # test it
    tdf = df.sample(8)
    predict = clf.predict(tdf[input_cols])
    answers = tdf[answer_col]

    print(list(zip(answers.values, predict)))

def populate_xls():
    wb_path = r"C:\Users\pants\PycharmProjects\FantasySports\mossixls\pitcher_grades_cals.xls"
    wb = openpyxl.load_workbook(wb_path, data_only=True)


def grade_id() -> pd.DataFrame:
    """
    Merge the grade and the name-to-ID tables together, making adjustments
    for ambiguous or duplicate matches.

    :return: merged data
    :rtype: pd.DataFrame
    """
    grade_df = pitcher_grade(path=os.path.join(fs, "mossi_data"))
    name_df = pitcher_names(csv=os.path.join(fs, "mossixls", "NAME_LOOKUP.csv"))

    grade_id_df = grade_df.merge(
        name_df,
        on='name',
        how='left',
        # how='outer',
        # indicator=True,
    )

    grade_id_df.drop(
        columns=[
            'testid',
            'spaces',
            'name_FL',
        ],
        inplace=True
    )

    return grade_id_df

def grade_war(grade_id_df) -> pd.DataFrame:
    """
    Merge the WAR data into the grade_id dataframe.
    https://www.baseball-reference.com/about/war_explained_glossary.shtml

    :param pd.DataFrame grade_id: the merged grade and ID dataframe
    :return: merged dataframe
    :rtype: pd.DataFrame
    """

    war_df = pitcher_war(
        csv=os.path.join(fs, "data", "WAR_pitching.csv")
    )
    grade_war_df = grade_id_df.merge(
        war_df,
        on=['playerID', 'year'],
        how='left',
        # indicator=True,
    )

    # drop row with year played outside year range (extra matches)
    grade_war_df = grade_war_df[(grade_war_df['year'].le(grade_war_df['last yr']) & grade_war_df['year'].ge(grade_war_df['first yr']))]

    # not blanks (this should be checked periodically)
    # nan = grade_war_df[grade_war_df['name_common'].isna()]
    grade_war_df = grade_war_df[~grade_war_df['name_common'].isna()]

    # drop 'team_ID' because it messes up later merge. 'NYN' is old Mets and 'NYM' is new Mets
    grade_war_df.drop(
        columns=[
            'team_ID',
        ],
        axis='columns',
        inplace=True,
    )

    return grade_war_df

def grade_war_stat(grade_war_df) -> pd.DataFrame:
    """
    Note: playerID are different
    O'donoghue, John is o'donjo02 and odonojo01

    :param grade_war_df:
    :return:
    """
    stats_df = pitcher_stats(
        csv=os.path.join(fs, r"baseballdatabank-master", "core", "Pitching.csv")
    )
    stats_df.convert_dtypes(convert_floating=True)
    stats_df.drop(
        columns=[
            'IPouts',
        ],
        axis='columns',
        inplace=True
    )

    grade_war_stat_df = grade_war_df.merge(
        stats_df,
        on=[
            'playerID',
            'year',
            'stint_ID',
            'G',
            'GS',
        ],
        how='left',
        indicator=True,
    )
    # nc_class(grade_war_stat_df)

    # # Check for data the "should" match
    i_na = grade_war_stat_df.loc[grade_war_stat_df['team_ID'].isna()].index
    w,s = (8, 17346)
    for c in grade_war_df.columns:
        if c in stats_df.columns:
            try:
                assert grade_war_df.loc[w][c] == stats_df.loc[s][c]
            except AssertionError:
                print(c, f"'{grade_war_df.loc[w][c]}'", f"'{stats_df.loc[s][c]}'")

    # get the names of the players with multiple stints
    names = grade_war_stat_df['player_ID'][grade_war_stat_df['stint_ID'] >= 2]
    # keep where the names are not
    df = grade_war_stat_df[~grade_war_stat_df['player_ID'].eq(names)]

    return grade_war_stat_df


if __name__ == '__main__':

    grade_id_df = grade_id()

    grade_war_df = grade_war(grade_id_df=grade_id_df)

    # grade_war_stat_df = grade_war_stat(grade_war_df=grade_war_df)

    log.debug('done building data')

    nc_classify(grade_war_df)

    log.debug('end program')
