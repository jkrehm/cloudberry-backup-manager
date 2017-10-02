# -*- coding: utf-8 -*-
from models.base import Base
from sqlalchemy import *


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    cbb_path = Column(String)