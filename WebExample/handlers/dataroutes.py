from flask import request,render_template
import json
import pandas as pd
import pickle
import os
import sys
sys.path.append('../MLDIR')
import manage

from matplotlib import pyplot as plt

import base64
from io import BytesIO

from matplotlib.figure import Figure

flag=0
df = None

def init_df():
    global df,flag

    if flag  == 0:
        flag = 1
        df = pd.read_csv('WebExample/data/rstate.csv').head(20)

def configure(app):

    @app.route('/')
    def hello_world():
        global df
        init_df()
        marketsInC = manage.getBlobsNames()
        return render_template('main.html',data=marketsInC)

    @app.route('/addnew')
    def add_new():
        return render_template('addnew.html')


    @app.route('/recordNewData')
    def recordNewData():
        return render_template('recordNewData.html')

    @app.route('/admin')
    def admin():
        return render_template('admin.html')

    @app.route('/details/<int:id>')
    def getdetails(id):
        global df
        return render_template('details.html',item=df.iloc[id])

    @app.route('/additem',methods=['POST'])
    def additem():
        global df
        market = request.form['market'].upper()
        candleKind = request.form['candleKind'].lower()
        predPeriods = int(request.form['predPeriods'])
        neurons = int(request.form['neurons'])
        activefunc = request.form['activefunc']
        numEpochs = int(request.form['numEpochs'])
        batchSize = int(request.form['batchSize'])
        optimizer = request.form['optimizer']
        



        results = manage.run_predictions(market, candleKind, predPeriods, neurons, activefunc, numEpochs, batchSize, optimizer)

        PEOPLE_FOLDER = os.path.join('static', 'charts')

        app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'foo.png')
        full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'foo2.png')

        # results = manage.justPrint()
        return render_template('ok.html', val=results[0], doss=results[1], user_image = full_filename, user_image2 = full_filename2)

    @app.route('/recordNewData',methods=['POST'])
    def predictitem():
        global df
        market = request.form['market'].upper()
        runNewrecording = request.form['btype']
        print(runNewrecording)
        recordstartDate = request.form['recoDate']
        
        minutesTorecord = int(request.form['minutesToRecord'])
        print(minutesTorecord)
        candleKind = request.form['candleKind']
        print(candleKind * 20)
        if runNewrecording == '1':
            print("Im in recording If")
            manage.recordNewData(market, minutesTorecord, recordstartDate, candleKind)
        else:
            print(runNewrecording * 100)
            manage.recordexistingMarket(market ,minutesTorecord, candleKind)
        print(market, runNewrecording, recordstartDate, candleKind)

        PEOPLE_FOLDER = os.path.join('static', 'charts')

        app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'lineChart.png')
        # full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'foo2.png')

        return render_template('res.html',val=market, user_image=full_filename)



    