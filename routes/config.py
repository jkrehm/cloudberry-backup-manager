from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

import db
import models

blueprint = Blueprint('config', __name__)


@blueprint.route('')
def config():
    return render_template('config.html')


@blueprint.route('/settings')
def settings():
    settings = db.session.query(models.Settings).first()
    return render_template('settings.html', settings=settings)


@blueprint.route('/settings/update', methods=['POST'])
def update_settings():
    to_save = request.form.to_dict()

    settings = db.session.query(models.Settings).first()
    updating = settings is not None
    if not updating:
        settings = models.Settings()

    settings.cbb_path = to_save['cbb_path']

    try:
        if updating:
            db.session.merge(settings)
        else:
            db.session.add(settings)
        db.session.commit()
        flash('Settings saved', category='success')
        return redirect(url_for('config.settings'))
    except IntegrityError:
        db.session.rollback()
        flash('Settings save failed', category='error')
    return redirect(url_for('config.settings'))


@blueprint.route('/accounts')
def accounts():
    accounts = db.session.query(models.Account)
    return render_template('accounts.html', accounts=accounts)


@blueprint.route('/account/add')
def add_account():
    return render_template('account.html', account=None)


@blueprint.route('/account/<string:account_id>')
def config_account(account_id):
    account = db.session.query(models.Account).filter(models.Account.id == account_id).first()
    if account is None:
        flash('Account does not exist', category='error')
        return redirect(url_for('config.accounts'))
    return render_template('account.html', account=account)


@blueprint.route('/account/update', methods=['POST'])
def update_account():
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
        return redirect(url_for('config.config_account', account_id=account.id))
    except IntegrityError:
        db.session.rollback()
        flash('Account creation failed', category='error')

    if updating:
        return redirect(url_for('config.config_account'))
    else:
        return redirect(url_for('config.add_account'))


@blueprint.route('/account/delete/<string:account_id>')
def delete_account(account_id):
    account = db.session.query(models.Account).filter(models.Account.id == account_id).first()
    try:
        db.session.delete(account)
        db.session.commit()
        flash('Account deleted', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('Account deletion failed', category='error')
    return redirect(url_for('config.accounts'))


@blueprint.route('/plans')
def plans():
    plans = db.session.query(models.Plan)
    return render_template('plans.html', plans=plans)


@blueprint.route('/plan/add')
def add_plan():
    accounts = db.session.query(models.Account).filter(models.Account.enabled)
    return render_template('plan.html', plan=None, accounts=accounts)


@blueprint.route('/plan/<string:plan_id>')
def config_plan(plan_id):
    plan = db.session.query(models.Plan).filter(models.Plan.id == plan_id)\
        .first()  # type: models.Plan
    if plan is None:
        flash('Plan does not exist', category='error')
        return redirect(url_for('config.plans'))
    accounts = db.session.query(models.Account).filter(models.Account.enabled)
    return render_template('plan.html', plan=plan, accounts=accounts)


@blueprint.route('/update/plan', methods=['POST'])
def update_plan():
    to_save = request.form.to_dict()
    updating = 'plan_id' in to_save

    if updating:
        plan = db.session.query(models.Plan).filter(models.Plan.id == to_save['plan_id']).first()
    else:
        plan = models.Plan()
    plan.name = to_save['name']
    plan.account_id = to_save['account_id']
    plan.enabled = 'enabled' in to_save
    plan.path = to_save['path']
    plan.exclude_sys = 'exclude_sys' in to_save
    plan.include_empty = 'include_empty' in to_save
    plan.include_masks = to_save['include_masks']
    plan.exclude_masks = to_save['exclude_masks']
    plan.encryption = to_save['encryption']
    plan.encryption_password = to_save['encryption_password']
    plan.purge = 'purge' in to_save
    plan.purge_recurrence = to_save['purge_recurrence']
    plan.keep_last_version = 'keep_last_version' in to_save
    plan.keep = to_save['keep']
    plan.delete = 'delete' in to_save
    plan.delete_delay = to_save['delete_delay']
    plan.repeat_every = to_save['repeat_every']
    plan.repeat_at = to_save['repeat_at']
    plan.repeat_day = to_save['repeat_day']
    plan.weekday = to_save['weekday'] if 'weekday' in to_save else ''
    plan.weeknumber = to_save['weeknumber']
    plan.use_rrs = 'use_rrs' in to_save
    plan.use_ia = 'use_ia' in to_save
    plan.use_sse = 'use_sse' in to_save
    plan.use_sta = 'use_sta' in to_save
    plan.use_compression = 'use_compression' in to_save
    plan.notification = to_save['notification']
    plan.subject = to_save['subject']

    try:
        if updating:
            db.session.merge(plan)
        else:
            db.session.add(plan)
        db.session.commit()
        flash('Plan saved', category='success')
        return redirect(url_for('config.config_plan', plan_id=plan.id))
    except IntegrityError:
        db.session.rollback()
        flash('Plan failed to save', category='error')

    if updating:
        return redirect(url_for('config.config_plan'))
    else:
        return redirect(url_for('config.add_plan'))


@blueprint.route('/plan/delete/<plan_id>')
def delete_plan(plan_id):
    plan = db.session.query(models.Plan).filter(models.Plan.id == plan_id).first()
    try:
        db.session.delete(plan)
        db.session.commit()
        flash('Plan deleted', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('Plan deletion failed', category='error')
    return redirect(url_for('config.plans'))
