# -*- coding: utf-8 -*-
from models import Base
import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'app.db')
engine = create_engine('sqlite:///{0}'.format(db_path), echo=False)

# Open session for database connection
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

if os.path.exists(db_path):
    Base.metadata.create_all(engine)
    # migrate_database()
    # clean_database()
else:
    try:
        Base.metadata.create_all(engine)
    except Exception:
        raise
