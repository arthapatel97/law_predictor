# from flask import Flask, render_template, request
# import mysql.connector
#
# mydb = mysql.connector.connect(user='root', password='password',
#                               host='localhost',
#                               database='Case_record')
#
#
#
# app = Flask(__name__)

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tabulate import tabulate
from sklearn.utils import resample
from sklearn import preprocessing

from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.metrics import roc_auc_score

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'Case_record'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/')
@app.route('/index/<name>')

def index():
    rows = ","
    if request.method == "POST":

        details = request.form
        query1 = details['docket_number']
        query2 = details['people_id']
        query22 = details['people_id_delete']
        query3 = details['location_id']
        query222 = details['people_name']
        query2222 = details['people_id_update']

        print("Details")

        cur = mysql.connection.cursor()
        if(not (query1 == "")):
            row = cur.execute("select * from Cases where docket_number = " + query1)
        if(not (query2 == "")):
            row = cur.execute("select * from people where people_id = " + query2)
        if(not (query22 == "")):
            row = cur.execute("delete from people where people_id = " + query22)

        if(not (query3 == "")):
            row = cur.execute("select * from location where location_id = " + query3)

        if(not (query222 == "")):
            row = cur.execute("insert into people(people_id, people_name) values(" + query222 + ")")

        if(not (query2222 == "")):
            query_arr = query2222.split(",")
            row = cur.execute("update people set people_id = "+ query_arr[1] + " where people_id = " + query_arr[0])


        print(query222)

        # row = cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        mysql.connection.commit()
        cur.close()

        # if(not (query22 == "")):
        #     rows = ""
        # else:
        #     rows = rows[0]

    return render_template('index.html',output = rows)

@app.route('/insert', methods=['GET', 'POST'])

def index2():
    law_records_df = pd.read_csv('law_record_data_cleaned.csv', sep=',')

    law_records_neg8_df = law_records_df.query('JUDGEMENT == -8')
    law_records_1_df = law_records_df.query('JUDGEMENT == 1')
    law_records_2_df = law_records_df.query('JUDGEMENT == 2')
    law_records_3_df = law_records_df.query('JUDGEMENT == 3')
    threshold = 3000

    law_records_neg8_df = resample(law_records_neg8_df,
                            replace = False,
                            n_samples = threshold,
                            random_state = 27)

    law_records_1_df = resample(law_records_1_df,
                            replace = False,
                            n_samples = law_records_1_df.shape[0],
                            random_state = 27)

    law_records_2_df = resample(law_records_2_df,
                            replace = False,
                            n_samples = law_records_2_df.shape[0],
                            random_state = 27)

    law_records_3_df = resample(law_records_3_df,
                            replace = False,
                            n_samples = law_records_3_df.shape[0],
                            random_state = 27)

    df_balanced = pd.concat([law_records_neg8_df, law_records_1_df, law_records_2_df, law_records_3_df])
    df_balanced = df_balanced.reset_index(drop=True)

    df_balanced.shape
    # print(df_balanced.shape)
    Y = df_balanced[['JUDGEMENT']].copy()
    X = df_balanced.drop(['JUDGEMENT'], axis=1).copy()
    # print(X)
    X = X.fillna(-999)
    Y = Y.fillna(3)
    X[['DEF']] = X[['DEF']].astype(str)
    X[['DISTRICT']] = X[['DISTRICT']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['FILEDATE']] = X[['FILEDATE']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['FDATEUSE']] = X[['FDATEUSE']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['SECTION']] = X[['SECTION']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['SUBSECT']] = X[['SUBSECT']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['JURY']] = X[['JURY']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['ARBIT']] = X[['ARBIT']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['MDLDOCK']] = X[['MDLDOCK']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['PLT']] = X[['PLT']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['DEF']] = X[['DEF']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['TRANSORG']] = X[['TRANSORG']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['TERMDATE']] = X[['TERMDATE']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['TDATEUSE']] = X[['TDATEUSE']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['TRMARB']] = X[['TRMARB']].apply(preprocessing.LabelEncoder().fit_transform)

# Perform a train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.1, random_state = 100)
    # print(len(y_train), len(X_train))

    feature_names = ['CIRCUIT', 'DISTRICT', 'OFFICE', 'DOCKET', 'ORIGIN', 'FILEDATE', 'FDATEUSE', 'JURIS',
                 'NOS', 'SECTION', 'SUBSECT', 'RESIDENC', 'JURY', 'CLASSACT', 'DEMANDED', 'COUNTY',
                 'ARBIT', 'MDLDOCK', 'PLT', 'DEF', 'TRANSOFF', 'TRANSDOC', 'TRANSORG', 'TERMDATE',
                 'TDATEUSE', 'TRCLACT', 'PROCPROG', 'DISP', 'NOJ', 'AMTREC', 'TRMARB', 'PROSE', 'TAPEYEAR']

    # Fit the DT Classifier to the data
    clf_gini = DecisionTreeClassifier(criterion="gini",
                                      random_state=100,
                                      max_depth=5,
                                      min_samples_leaf=10)

    clf_gini.fit(X_train, y_train)

    export_graphviz(clf_gini,
                    feature_names=feature_names,
                    filled=True,
                    rounded=True,
                    out_file='tree_gini.dot')

    # print(len(y_test))


    importantFeatures = sorted(zip(feature_names, clf_gini.feature_importances_), key=lambda x: x[1], reverse=True)
    # for feature in importantFeatures:
    #     print(feature)
    # print('Decision tree accuracy: %s' % clf_gini.score(X_test, y_test))
    print("hi")

    return render_template('index2.html')



if __name__ == '__main__':
    app.run(debug=True)
