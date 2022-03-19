from flask import request,render_template
import json
import pandas as pd
import pickle


def configure(app):

    @app.route('/')
    def hello_world():
        df = pd.DataFrame()
        return render_template('main.html',data=df)

    @app.route('/admin')
    def admin():
        return render_template('admin.html')

