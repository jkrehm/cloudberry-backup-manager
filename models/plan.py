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
            'addBackupPlan',
            '-n "' + self.name + '"',
            '-a "' + self.account.name + '"',
            '-en ' + 'yes' if self.enabled else 'no',
            '-rrs ' + 'yes' if self.use_rrs else 'no',
            '-standardIA ' + 'yes' if self.use_ia else 'no',
            '-sse ' + 'yes' if self.use_sse else 'no',
            '-sta ' + 'yes' if self.use_sta else 'no',
            '-f "' + self.path + '"'
        ]

        for exclusion in self.exclusions:
            cmd.append('-ef "' + exclusion.path + '"')

        cmd.append('-es ' + 'yes' if self.exclude_sys else 'no')
        cmd.append('-c ' + 'yes' if self.use_compression else 'no')

        if self.include_masks:
            cmd.append('-ifm "' + self.include_masks + '"')

        if self.exclude_masks:
            cmd.append('-efm "' + self.exclude_masks + '"')

        if self.encryption:
            cmd.append('-ea "' + self.encryption + '"')
            cmd.append('-ep "' + self.encryption_password + '"')

        cmd.append('-bef ' + 'yes' if self.include_empty else 'no')

        if self.purge:
            cmd.append('-purge "' + self.purge_recurrence + '"')
            cmd.append('-keepLastVersion ' + 'yes' if self.keep_last_version else 'no')
            if self.keep > 0:
                cmd.append('-keep "' + self.keep + '"')

        cmd.append('-dl ' + 'yes' if self.delete else 'n')
        if self.delete:
            cmd.append('-dld "' + str(self.delete_delay) + '"')

        cmd.append('-every "' + self.repeat_every + '"')
        cmd.append('-at "' + self.repeat_at + '"')

        cmd.append('-notification "' + self.notification + '"')
        cmd.append('-subject "' + self.subject + '"')

        return ' '.join(cmd).replace(';', ' ')

    def generate_edit_command(self):
        return 'editBackupPlan'

    def generate_delete_command(self):
        return 'deletePlan'
