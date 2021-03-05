#!/usr/env/bin python
"""
Mossi database models
"""
import os
import logging
from peewee import *
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL',
                            'sqlite:///mossi.db'))

class BaseModel(Model):
    class Meta:
        database = db

class Player(BaseModel):
    name = CharField(primary_key=True, max_length=48)
    player_ID = CharField(max_length=8)
    mlb_ID = IntegerField()

class Team(BaseModel):
    name = CharField(primary_key=True, )
    league = CharField(max_length=2)
    owner = CharField(max_length=48)
    email = CharField(max_length=128)
    phone = CharField(max_length=12)

class Roser(BaseModel):
    team = ForeignKeyField(Team, backref='roster')
    players = ManyToManyField(Player, backref='roster')

class MossiPlayerStat(BaseModel):
    name = ManyToManyField(Player, backref='stats')
    master_team = ManyToManyField(Player, backref='stats')
    year = IntegerField()
    Tm = CharField(max_length=3)
    Lg = CharField(max_length=2)
    AVG = FloatField()
    OBP = FloatField()
    SLG = FloatField()
    OPS = FloatField()
    ISO = FloatField()
    SECA = FloatField()
    TA = FloatField()
    RCON = FloatField()
    RC = FloatField()
    RC_G = FloatField()
    PA = IntegerField()
    IBB = IntegerField()
    HBP = IntegerField()
    SH = IntegerField()
    SF = IntegerField()
    G = IntegerField()
    AB = IntegerField()
    R = IntegerField()
    H = IntegerField()
    DBL = IntegerField()
    TPL = IntegerField()
    HR = IntegerField()
    TB = IntegerField()
    RBI = IntegerField()
    SO = IntegerField()
    BB = IntegerField()
    ASB = IntegerField()
    SB = IntegerField()
    CS = IntegerField()
    SBP = FloatField()
    GDP = IntegerField()
