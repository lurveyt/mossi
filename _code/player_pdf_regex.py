#!/usr/bin/env python
"""
Copy both pitching and batting pdfs to a new YYYY_draft_raw.txt
ADD extra new line at the end of file
run code
remove header lines
"""


import re

year = 1988
filex = r"..\mossi_data\draft\{}_draft_raw.txt".format(
    year)

text_raw = open(filex, 'r').read()

patrn = "{Name}\s{Age}\s{Pos}\s{D}\s{B}\s{Sp}\s{Th}\s?{Arm}\s?{T}\s?{Grade}\s?{Ctrl}\s?{HR}\s?\n".format(
    Name=r"(?P<Name>[A-Za-z]+,.+?[A-Za-z]{1,}\s?\w?\.?)",
    Age=r"(?P<Age>(?:\d\d)|(?:0))",
    Pos=r"(?P<Pos>[A-Z0-9][A-Z]?\+?)",
    D=r"(?P<D>\d\d?)",
    B=r"(?P<B>[LRB])",
    Sp=r"(?P<Sp>\d\d?)",
    Th=r"(?P<Th>[-\+]\d)?",
    Arm=r"(?P<Arm>\d+)?",
    T=r"(?P<T>[LRB])",
    Grade=r"(?P<Grade>\d?\d?\/?\d+\s?\*?)?",
    Ctrl=r"(?P<Ctrl>\w+)?",
    HR=r"(?P<HR>[A-Z])?")

# found = re.findall(pattern=patrn, string=text_raw)    ## DEBUG

# set delimiter
delimiters = {'TAB': "\t", 'SEMICOL': ";", 'COMMA': ","}

# Delete Header Lines
text_strip = re.sub(pattern="\d{1,2}\/\d{1,2}\/\d{4}.+?\n", repl="", string=text_raw)
text_strip = re.sub(pattern="Player Name.+?\n", repl="", string=text_strip)

# sub all the player info
for key, DE in delimiters.items():
    rplce = "\g<Name> {0}\g<Age>{0}\g<Pos>{0}\g<D>{0}\g<B>{0}\g<Sp>{0}\g<Th>{0}\g<Arm>{0}\g<T>{0}\g<Grade>{0}\g<Ctrl>{0}\g<HR>\n".format(DE)
    sub_text = re.sub(pattern=patrn, repl=rplce, string=text_strip)

    # sub on the title line
    sub_text = re.sub(pattern="Player\sName\sAge\sPos\sD\sB\sSp\sTh\sArm\sT\sGrade\sCtrl\sHR\sTm\sLg",
                      repl="Player Name{0}Age{0}Pos{0}D{0}B{0}Sp{0}Th{0}Arm{0}T{0}Grade{0}Ctrl{0}HR{0}Tm{0}Lg".format(DE),
                      string=sub_text)

    print(sub_text)

    with open(filex.replace("raw", key), "w") as W:
        W.write(sub_text)
