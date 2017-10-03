from db import db


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    enabled = db.Column(db.Boolean)
    type = db.Column(db.String(30))
    access_key = db.Column(db.String(20))
    secret_key = db.Column(db.String(40))
    bucket = db.Column(db.String)
    prefix = db.Column(db.String)
    use_ssl = db.Column(db.Boolean)

    def generate_add_command(self):
        return 'addAccount'

    def generate_edit_command(self):
        return 'editAccount'

    def generate_delete_command(self):
        return 'deleteAccount'
