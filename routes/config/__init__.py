from flask import Blueprint, render_template

blueprint = Blueprint('config', __name__)


@blueprint.route('')
def config():
    return render_template('config.html')
