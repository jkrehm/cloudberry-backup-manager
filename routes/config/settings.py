import models

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

blueprint = Blueprint('config_settings', __name__)


@blueprint.route('')
def settings(db: SQLAlchemy):
    settings = db.session.query(models.Settings).first()
    return render_template('settings.html', settings=settings)


@blueprint.route('/update', methods=['POST'])
def update_settings(db: SQLAlchemy):
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
        return redirect(url_for('config_settings.settings'))
    except IntegrityError:
        db.session.rollback()
        flash('Settings save failed', category='error')
    return redirect(url_for('config_settings.settings'))