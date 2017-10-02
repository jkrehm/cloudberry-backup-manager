#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask

from routes.config import blueprint as config_blueprint

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'b3D$EJAQ4g91U8UPqwZ4yaaSoAsH!V')

app.register_blueprint(config_blueprint, url_prefix='/config')

if __name__ == '__main__':
    app.run()
