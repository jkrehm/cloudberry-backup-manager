from typing import List

# from sqlalchemy import *
# from sqlalchemy.orm import relationship

from db import db
from models.account import Account
from models.plan_exclusion import PlanExclusion
from models.settings import Settings


class Plan(db.Model):
    __tablename__ = 'plan'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    account_id = db.Column(db.String(64), db.ForeignKey('account.id'))
    enabled = db.Column(db.Boolean)
    path = db.Column(db.String)
    exclude_sys = db.Column(db.Boolean)
    include_empty = db.Column(db.Boolean)
    include_masks = db.Column(db.String)
    exclude_masks = db.Column(db.String)
    encryption = db.Column(db.String(10))
    encryption_password = db.Column(db.String)
    purge = db.Column(db.Boolean)
    purge_recurrence = db.Column(db.String(5))
    keep_last_version = db.Column(db.Boolean)
    keep = db.Column(db.Integer)
    delete = db.Column(db.Boolean)
    delete_delay = db.Column(db.Integer)
    repeat_every = db.Column(db.String(10))
    repeat_at = db.Column(db.String(30))
    repeat_day = db.Column(db.Integer)
    weekday = db.Column(db.String(30))
    weeknumber = db.Column(db.String(10))
    use_rrs = db.Column(db.Boolean)
    use_ia = db.Column(db.Boolean)
    use_sse = db.Column(db.Boolean)
    use_sta = db.Column(db.Boolean)
    use_compression = db.Column(db.Boolean)
    notification = db.Column(db.String(10))
    subject = db.Column(db.String(64))

    account = db.relationship('Account')  # type: Account
    exclusions = db.relationship('PlanExclusion')  # type: List[PlanExclusion]

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

        # addBackupPlan
        # -n planName
        # -a <accountName | accountID>
        # [-en <yes | no>]
        # [[-rrs <yes | no>] | [-standardIA <yes | no>]]
        # [-sse <yes | no>]
        # [-sta <yes | no>]
        # -f <pathToFile | pathToDir>
        # -ef <pathToFile | pathToDir>
        # [-es <yes | no>]
        # [-c <yes | no>]
        # [-ifm Filters| -efm Filters]
        # [-ea <AES_128 | AES_192 | AES_256 | no > -ep password]
        # [-bef <yes | no>]
        # [-purge delete_after_time
        #   -keepLastVersion <yes | no>
        #   -keep keep_versions_number]
        # [-dl <yes
        #   -dld delete_locally_deleted_delay | no >]
        # [
        #   [
        #       [-every [day, week, month, dayofmonth] <
        #           -workTime xx:xx-xx:xx
        #               -recurrencePeriod period |
        #           -at timeOfDay
        #       >]
        #       [-day [1..31]
        #   ]
        #   [-weekday list ofWeekDays]
        #   [-weeknumber weeknumber]
        # ] |
        #   -at onceDateTime] ]
        # [-repeateEvery NumOfMonthes
        #   -repeatFrom FromDate]
        # [-notification <errorOnly | on | off>]
        # [-subject Subject]

        return cmd

    def generate_edit_command(self):
        return 'editBackupPlan'

    def generate_delete_command(self):
        return 'deletePlan'
