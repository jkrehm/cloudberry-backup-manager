# -*- coding: utf-8 -*-
from models.base import Base
from sqlalchemy import *


class PlanExclusion(Base):
    __tablename__ = 'plan_exclusion'

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plan.id'))
    path = Column(String)
