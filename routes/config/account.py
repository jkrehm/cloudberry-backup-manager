import models

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

blueprint = Blueprint('config_account', __name__)


@blueprint.route('/all')
def view_all(db: SQLAlchemy):
    accounts = db.session.query(models.Account)
    return render_template('accounts.html', accounts=accounts)


@blueprint.route('/add')
def add_account():
    return render_template('account.html', account=None)


@blueprint.route('/<string:account_id>')
def config_account(account_id, db: SQLAlchemy):
    account = db.session.query(models.Account).filter(models.Account.id == account_id).first()
    if account is None:
        flash('Account does not exist', category='error')
        return redirect(url_for('config_account.view_all'))
    return render_template('account.html', account=account)


@blueprint.route('/update', methods=['POST'])
def update_account(db: SQLAlchemy):
    to_save = request.form.to_dict()
    updating = 'account_id' in to_save

    if updating:
        account = db.session.query(models.Account).filter(models.Account.id == to_save['account_id']).first()
    else:
        account = models.Account()
    account.name = to_save['name']
    account.enabled = 'enabled' in to_save
    account.type = to_save['type']
    account.access_key = to_save['access_key']
    account.secret_key = to_save['secret_key']
    account.bucket = to_save['bucket']
    account.prefix = to_save['prefix']
    account.use_ssl = 'use_ssl' in to_save

    try:
        if updating:
            db.session.merge(account)
        else:
            db.session.add(account)
        db.session.commit()
        flash('Account created', category='success')
        return redirect(url_for('config_account.config_account', account_id=account.id))
    except IntegrityError:
        db.session.rollback()
        flash('Account creation failed', category='error')

    if updating:
        return redirect(url_for('config_account.config_account'))
    else:
        return redirect(url_for('config_account.add_account'))


@blueprint.route('/delete/<string:account_id>')
def delete_account(account_id, db: SQLAlchemy):
    account = db.session.query(models.Account).filter(models.Account.id == account_id).first()
    try:
        db.session.delete(account)
        db.session.commit()
        flash('Account deleted', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('Account deletion failed', category='error')
    return redirect(url_for('config_account.view_all'))
