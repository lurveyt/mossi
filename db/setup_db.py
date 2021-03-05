#!/usr/env/bin python
"""setup the database"""
from db.models import *

database = SqliteDatabase('mossi.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only