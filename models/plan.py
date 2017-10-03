# -*- coding: utf-8 -*-
from typing import List

from sqlalchemy import *
from sqlalchemy.orm import relationship

import db
from models.account import Account
from models.base import Base
from models.plan_exclusion import PlanExclusion
from models.settings import Settings


class Plan(Base):
    __tablename__ = 'plan'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    account_id = Column(String(64), ForeignKey('account.id'))
    enabled = Column(Boolean)
    path = Column(String)
    exclude_sys = Column(Boolean)
    include_empty = Column(Boolean)
    include_masks = Column(String)
    exclude_masks = Column(String)
    encryption = Column(String(10))
    encryption_password = Column(String)
    purge = Column(Boolean)
    purge_recurrence = Column(String(5))
    keep_last_version = Column(Boolean)
    keep = Column(Integer)
    delete = Column(Boolean)
    delete_delay = Column(Integer)
    repeat_every = Column(String(10))
    repeat_at = Column(String(30))
    repeat_day = Column(Integer)
    weekday = Column(String(30))
    weeknumber = Column(String(10))
    use_rrs = Column(Boolean)
    use_ia = Column(Boolean)
    use_sse = Column(Boolean)
    use_sta = Column(Boolean)
    use_compression = Column(Boolean)
    notification = Column(String(10))
    subject = Column(String(64))

    account = relationship('Account')  # type: Account
    exclusions = relationship('PlanExclusion')  # type: List[PlanExclusion]

    def generate_add_command(self):
        settings = db.session.query(Settings).first()

        cmd = [
            settings.cbb_path,
            'addBackupPlan'
        ]
        cmd += ['-n', self.name]
        cmd += ['-a', self.account.name]
        cmd += ['-en ', 'yes' if self.enabled else 'no']
        cmd += ['-rrs ', 'yes' if self.use_rrs else 'no']
        cmd += ['-standardIA ', 'yes' if self.use_ia else 'no']
        cmd += ['-sse ', 'yes' if self.use_sse else 'no']
        cmd += ['-sta ', 'yes' if self.use_sta else 'no']
        cmd += ['-f', self.path] 

        for exclusion in self.exclusions:
            cmd += ['-ef', exclusion.path]

        cmd += ['-es ', 'yes' if self.exclude_sys else 'no']
        cmd += ['-c ', 'yes' if self.use_compression else 'no']

        if self.include_masks:
            cmd += ['-ifm', self.include_masks]

        if self.exclude_masks:
            cmd += ['-efm', self.exclude_masks]

        if self.encryption:
            cmd += ['-ea', self.encryption]
            cmd += ['-ep', self.encryption_password]

        cmd += ['-bef ', 'yes' if self.include_empty else 'no']

        if self.purge:
            cmd += ['-purge', self.purge_recurrence]
            cmd += ['-keepLastVersion ', 'yes' if self.keep_last_version else 'no']
            if self.keep > 0:
                cmd += ['-keep', self.keep]

        cmd += ['-dl ', 'yes' if self.delete else 'n']
        if self.delete:
            cmd += ['-dld', str(self.delete_delay)]

        cmd += ['-every', self.repeat_every]
        cmd += ['-at', self.repeat_at]

        cmd += ['-notification', self.notification]
        cmd += ['-subject', self.subject]

        return cmd

    def generate_edit_command(self):
        return 'editBackupPlan'

    def generate_delete_command(self):
        return 'deletePlan'
