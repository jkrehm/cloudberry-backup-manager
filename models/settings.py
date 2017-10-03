# -*- coding: utf-8 -*-
from db import db


class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    cbb_path = db.Column(db.String)