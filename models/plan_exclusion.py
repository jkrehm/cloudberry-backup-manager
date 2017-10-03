# -*- coding: utf-8 -*-
from db import db


class PlanExclusion(db.Model):
    __tablename__ = 'plan_exclusion'

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    path = db.Column(db.String)
