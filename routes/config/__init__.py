from flask import Blueprint, render_template

blueprint = Blueprint('config', __name__, template_folder='templates/config')


@blueprint.route('')
def config():
    return render_template('config/config.html')
