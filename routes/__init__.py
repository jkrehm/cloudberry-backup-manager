from flask import Blueprint, render_template

blueprint = Blueprint('main', __name__)


@blueprint.route('')
def main():
    return render_template('main.html')
