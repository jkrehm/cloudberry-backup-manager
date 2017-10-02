# -*- coding: utf-8 -*-
from models.base import Base
from sqlalchemy import *


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    enabled = Column(Boolean)
    type = Column(String(30))
    access_key = Column(String(20))
    secret_key = Column(String(40))
    bucket = Column(String)
    prefix = Column(String)
    use_ssl = Column(Boolean)

    def generate_add_command(self):
        return 'addAccount'

    def generate_edit_command(self):
        return 'editAccount'

    def generate_delete_command(self):
        return 'deleteAccount'