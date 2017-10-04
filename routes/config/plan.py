import models

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

blueprint = Blueprint('config_plan', __name__)


@blueprint.route('/all')
def view_all(db: SQLAlchemy):
    plans = db.session.query(models.Plan)
    return render_template('plans.html', plans=plans)


@blueprint.route('/add')
def add_plan(db: SQLAlchemy):
    accounts = db.session.query(models.Account).filter(models.Account.enabled)
    return render_template('plan.html', plan=None, accounts=accounts)


@blueprint.route('/<string:plan_id>')
def config_plan(plan_id, db: SQLAlchemy):
    plan = db.session.query(models.Plan).filter(models.Plan.id == plan_id) \
        .first()  # type: models.Plan
    if plan is None:
        flash('Plan does not exist', category='error')
        return redirect(url_for('config_plan.view_all'))
    cmd = plan.generate_add_command()
    accounts = db.session.query(models.Account).filter(models.Account.enabled)
    return render_template('plan.html', plan=plan, accounts=accounts)


@blueprint.route('/update', methods=['POST'])
def update_plan(db: SQLAlchemy):
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
        return redirect(url_for('config_plan.config_plan', plan_id=plan.id))
    except IntegrityError:
        db.session.rollback()
        flash('Plan failed to save', category='error')

    if updating:
        return redirect(url_for('config_plan.config_plan'))
    else:
        return redirect(url_for('config_plan.add_plan'))


@blueprint.route('/delete/<plan_id>')
def delete_plan(plan_id, db: SQLAlchemy):
    plan = db.session.query(models.Plan).filter(models.Plan.id == plan_id).first()
    try:
        db.session.delete(plan)
        db.session.commit()
        flash('Plan deleted', category='success')
    except IntegrityError:
        db.session.rollback()
        flash('Plan deletion failed', category='error')
    return redirect(url_for('config_plan.view_all'))
