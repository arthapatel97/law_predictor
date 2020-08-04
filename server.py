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
    sql_select_Query = "select * from training_model"
    cursor = mysql.connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    law_records_df = pd.DataFrame(records, columns=["JURIS", "NOS", "SECTION", "DISTRICT", "ORIGIN", "DOCKET", "RESIDENC", "TAPEYEAR", "FILEDATE", "PLT", "TDATEUSE", "OFFICE", "DEMANDED", "COUNTY", "JUDGEMENT"])
    print(law_records_df)

    # law_records_df = pd.read_csv('law_record_data_cleaned.csv', sep=',')

    # law_records_neg8_df = law_records_df.query('JUDGEMENT == -8')
    law_records_1_df = law_records_df.query('JUDGEMENT == 1')
    law_records_2_df = law_records_df.query('JUDGEMENT == 2')
    law_records_3_df = law_records_df.query('JUDGEMENT == 3')

    # threshold = 1300
    #
    # law_records_neg8_df = resample(law_records_neg8_df,
    #                         replace = False,
    #                         n_samples = threshold,
    #                         random_state = 27)


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

    # df_balanced = pd.concat([law_records_neg8_df, law_records_1_df, law_records_2_df, law_records_3_df])
    df_balanced = pd.concat([law_records_1_df, law_records_2_df, law_records_3_df])
    df_balanced = df_balanced.reset_index(drop=True)

    df_balanced.shape
    # print(df_balanced.shape)
    Y = df_balanced[['JUDGEMENT']].copy()
    X = df_balanced.drop(['JUDGEMENT'], axis=1).copy()
    # print(X)
    X = X.fillna(-999)
    Y = Y.fillna(3)
    # X[['DEF']] = X[['DEF']].astype(str)
    X[['DISTRICT']] = X[['DISTRICT']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['FILEDATE']] = X[['FILEDATE']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['FDATEUSE']] = X[['FDATEUSE']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['SECTION']] = X[['SECTION']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['SUBSECT']] = X[['SUBSECT']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['JURY']] = X[['JURY']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['ARBIT']] = X[['ARBIT']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['MDLDOCK']] = X[['MDLDOCK']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['PLT']] = X[['PLT']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['DEF']] = X[['DEF']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['TRANSORG']] = X[['TRANSORG']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['TERMDATE']] = X[['TERMDATE']].apply(preprocessing.LabelEncoder().fit_transform)
    X[['TDATEUSE']] = X[['TDATEUSE']].apply(preprocessing.LabelEncoder().fit_transform)
    # X[['TRMARB']] = X[['TRMARB']].apply(preprocessing.LabelEncoder().fit_transform)

# Perform a train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.1, random_state = 100)
    # print(len(y_train), len(X_train))
    # print(X_test.iloc[0])
    feature_names = ['DISTRICT', 'OFFICE', 'DOCKET', 'ORIGIN', 'FILEDATE', 'JURIS',
                 'NOS', 'SECTION', 'RESIDENC', 'DEMANDED', 'COUNTY',
                 'PLT','TDATEUSE','TAPEYEAR']

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
    for feature in importantFeatures:
        print(feature)


    print('Decision tree accuracy: %s' % clf_gini.score(X_test, y_test))
    # print("hi")

    # test_case = pd.Series([2,56,5,9700614,1,1273,99,4,95,40,0,12,0,-8,0,36067,0,0,487,3032,-8,-8,0,1473,78,-8,2,4,2,250,0,0,1997], index=['CIRCUIT', 'DISTRICT', 'OFFICE', 'DOCKET', 'ORIGIN', 'FILEDATE', 'FDATEUSE', 'JURIS',
    #              'NOS', 'SECTION', 'SUBSECT', 'RESIDENC', 'JURY', 'CLASSACT', 'DEMANDED', 'COUNTY',
    #              'ARBIT', 'MDLDOCK', 'PLT', 'DEF', 'TRANSOFF', 'TRANSDOC', 'TRANSORG', 'TERMDATE',
    #              'TDATEUSE', 'TRCLACT', 'PROCPROG', 'DISP', 'NOJ', 'AMTREC', 'TRMARB', 'PROSE', 'TAPEYEAR'], name=6159402)

    test_case = X_test.iloc[0]
    a  = ""
    if request.method == "POST":
        details = request.form

        if(not (details['district'] == "")):
            test_case['DISTRICT'] = details['district']

        if(not (details['office'] == "")):
            test_case['OFFICE'] = details['office']

        if(not (details['demanded'] == "")):
            test_case['DEMANDED'] = details['demanded']

        if(not (details['juris'] == "")):
            test_case['JURIS'] = details['juris']

        if(not (details['origin'] == "")):
            test_case['ORIGIN'] = details['origin']

        if(not (details['residenc'] == "")):
            test_case['RESIDENC'] = details['residenc']

        if(not (details['nos'] == "")):
            test_case['NOS'] = details['nos']

        if(not (details['section'] == "")):
            test_case['SECTION'] = details['section']

        if(not (details['county'] == "")):
            test_case['COUNTY'] = details['county']


    # # print(X_test.iloc[0])
    # result = clf_gini.predict([test_case])
    # test_case['NOJ'] = -8
    # test_case['DISP'] = 6
    # test_case['AMTREC'] = 0
        # test_case['JURIS']= 1
        # # test_case['DISTRICT']= 87
        # test_case['PLT'] = 'UNITED STATES OF'
        # test_case['NOS'] = 140
        # # test_case['DEF'] = 'MISSOURI PACIFIC RR'
        # # test_case['SUBSECT']= -8
        # test_case['COUNTY']= 36047
        # le = preprocessing.LabelEncoder()
        # encoded_strings = le.fit_transform([test_case['PLT']])
        #
        # test_case['PLT'] = encoded_strings[0]
    # test_case['DEF'] = encoded_strings[1]


    # print(result)

        if((details['district'] == "") and (details['county'] == "") and (details['demanded'] == "") and (details['juris'] == "") and (details['origin'] == "") and (details['residenc'] == "") and (details['nos'] == "") and (details['section'] == "") and (details['county'] == "")):
            a = "All fields empty!"
        else:
            a = clf_gini.predict([test_case])
        print(a)

    return render_template('index2.html', output = a, result = 'Decision tree accuracy: %s' % clf_gini.score(X_test, y_test))



if __name__ == '__main__':
    app.run(debug=True)
