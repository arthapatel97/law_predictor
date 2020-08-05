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

def index_home():
    return render_template('index.html')


@app.route('/delete.html', methods=['GET', 'POST'])

def index_delete():
    rows = ","
    if request.method == "POST":
        details = request.form

        query_people_id_select = details['people_id']
        query_people_name_select = details['people_name']
        query_location_id_select = details['location_id']
        query_circuit_select = details['circuit']
        query_district_select = details['district']
        query_office_select = details['office']
        query_people_of_interest_id_select = details['people_of_interest_id']
        query_plaintiff_id_select = details['plaintiff_id']

        query_defendant_id_select = details['defendant_id']
        query_docket_number_select = details['docket_number']
        query_case_name_select = details['case_name']
        query_filing_date_select = details['filing_date']
        query_termination_date_select = details['termination_date']
        query_disposition_select = details['disposition']
        query_nature_of_judgement_select = details['nature_of_judgement']
        query_judgement_select = details['judgement']

        wheres = []
        table_string = ""
        where_string = ""

        if (not (query_people_id_select == "")):
            table_string = "people"
            wheres.append("people_id = " + query_people_id_select)

        if (not (query_people_name_select == "")):
            table_string = "people"
            wheres.append("people_name = '" + query_people_name_select + "'")

        if (not (query_location_id_select == "")):
            table_string = "location"
            wheres.append("location_id = " + query_location_id_select)

        if (not (query_circuit_select == "")):
            table_string = "location"
            wheres.append("circuit = " + query_circuit_select)

        if (not (query_district_select == "")):
            table_string = "location"
            wheres.append("district = " + query_district_select)

        if (not (query_office_select == "")):
            table_string = "location"
            wheres.append("office = " + query_office_select)

        if (not (query_people_of_interest_id_select == "")):
            table_string = "people_of_interest"
            wheres.append("people_of_interest_id = " + query_people_of_interest_id_select)

        if (not (query_plaintiff_id_select == "")):
            table_string = "people_of_interest"
            wheres.append("plaintiff_id = " + query_plaintiff_id_select)

        if (not (query_defendant_id_select == "")):
            table_string = "people_of_interest"
            wheres.append("defendant_id = " + query_defendant_id_select)

        if (not (query_docket_number_select == "")):
            table_string = "Cases"
            wheres.append("docket_number = " + query_docket_number_select)

        if (not (query_case_name_select == "")):
            table_string = "Cases"
            wheres.append("case_name = '" + query_case_name_select + "'")

        if (not (query_filing_date_select == "")):
            table_string = "Cases"
            wheres.append("filing_date = '" + query_filing_date_select + "'")

        if (not (query_termination_date_select == "")):
            table_string = "Cases"
            wheres.append("termination_date = '" + query_termination_date_select + "'")

        if (not (query_disposition_select == "")):
            table_string = "Cases"
            wheres.append("disposition = " + query_disposition_select)

        if (not (query_nature_of_judgement_select == "")):
            table_string = "Cases"
            wheres.append("nature_of_judgement = " + query_nature_of_judgement_select)


        if (not (query_judgement_select == "")):
            table_string = "Cases"
            wheres.append("judgement = " + query_judgement_select)


        for where in wheres:
            if where_string != "":
                where_string += " and " + where
            else:
                where_string = where

        delete_query = "delete from " + table_string + " where " + where_string
        print(delete_query)

        cur = mysql.connection.cursor()
        row = cur.execute(delete_query)

        mysql.connection.commit()
        cur.close()

    return render_template('delete.html')


@app.route('/insert.html', methods=['GET', 'POST'])

def index_insert():
    rows = ","
    if request.method == "POST":
        details = request.form

        query_people_id_select = details['people_id']
        query_people_name_select = details['people_name']
        query_location_id_select = details['location_id']
        query_circuit_select = details['circuit']
        query_district_select = details['district']
        query_office_select = details['office']
        query_people_of_interest_id_select = details['people_of_interest_id']
        query_plaintiff_id_select = details['plaintiff_id']
        query_defendant_id_select = details['defendant_id']
        query_docket_number_select = details['docket_number']
        query_case_name_select = details['case_name']
        query_filing_date_select = details['filing_date']
        query_termination_date_select = details['termination_date']
        query_disposition_select = details['disposition']
        query_nature_of_judgement_select = details['nature_of_judgement']
        query_judgement_select = details['judgement']

        wheres = []
        table_string = ""
        value_string = ""
        column_string = ""

        if (not (query_people_id_select == "")):
            table_string = "people"
            if(value_string==""):
                value_string = query_people_id_select
                column_string="people_id"
            else:
                value_string += ", " + query_people_id_select
                column_string += ", people_id"

        if (not (query_people_name_select == "")):
            table_string = "people"
            if(value_string==""):
                value_string = "'"+ query_people_name_select+"'"
                column_string= "people_name"
            else:
                value_string += ", '" + query_people_name_select +"'"
                column_string += ", people_name"


        if (not (query_location_id_select == "")):
            table_string = "location"
            if(value_string==""):
                value_string = query_location_id_select
                column_string= "location_id"
            else:
                value_string += ", " + query_location_id_select
                column_string += ", location_id"


        if (not (query_circuit_select == "")):
            table_string = "location"
            if(value_string==""):
                value_string = query_circuit_select
                column_string= "circuit"
            else:
                value_string += ", " + query_circuit_select
                column_string += ", circuit"


        if (not (query_district_select == "")):
            table_string = "location"
            if(value_string==""):
                value_string = query_district_select
                column_string= "district"
            else:
                value_string += ", " + query_district_select
                column_string += ", district"

        if (not (query_office_select == "")):
            table_string = "location"
            if(value_string==""):
                value_string = query_office_select
                column_string= "office"
            else:
                value_string += ", " + query_office_select
                column_string += ", office"


        if (not (query_people_of_interest_id_select == "")):
            table_string = "people_of_interest"
            if(value_string==""):
                value_string = query_people_of_interest_id_select
                column_string= "people_of_interest_id"
            else:
                value_string += ", " + query_people_of_interest_id_select
                column_string += ", people_of_interest_id"

        if (not (query_plaintiff_id_select == "")):
            table_string = "people_of_interest"
            if(value_string==""):
                value_string = query_plaintiff_id_select
                column_string= "plaintiff_id"
            else:
                value_string += ", " + query_plaintiff_id_select
                column_string += ", plaintiff_id"


        if (not (query_defendant_id_select == "")):
            table_string = "people_of_interest"
            if(value_string==""):
                value_string = query_defendant_id_select
                column_string= "defendant_id"
            else:
                value_string += ", " + query_defendant_id_select
                column_string += ", defendant_id"

        if (not (query_docket_number_select == "")):
            table_string = "Cases"
            if(value_string==""):
                value_string = query_docket_number_select
                column_string= "docket_number"
            else:
                value_string += ", " + query_docket_number_select
                column_string += ", docket_number"


        if (not (query_case_name_select == "")):
            table_string = "Cases"
            if(value_string==""):
                value_string = query_case_name_select
                column_string= "case_name"
            else:
                value_string += ", '" + query_case_name_select + "'"
                column_string += ", case_name"


        if (not (query_filing_date_select == "")):
            table_string = "Cases"
            if(value_string==""):
                value_string = "'"+ query_filing_date_select +"'"
                column_string= "filing_date"
            else:
                value_string += ", '" + query_filing_date_select +"'"
                column_string += ", filing_date"

        if (not (query_termination_date_select == "")):
            table_string = "Cases"
            if(value_string==""):
                value_string = "'" + query_termination_date_select+ "'"
                column_string= "termination_date"
            else:
                value_string += ", '" + query_termination_date_select + "'"
                column_string += ", termination_date"


        if (not (query_disposition_select == "")):
            table_string = "Cases"
            if(value_string==""):
                value_string = query_disposition_select
                column_string= "disposition"
            else:
                value_string += ", " + query_disposition_select
                column_string += ", disposition"

        if (not (query_nature_of_judgement_select == "")):
            table_string = "Cases"
            if(value_string==""):
                value_string = query_nature_of_judgement_select
                column_string= "nature"
            else:
                value_string += ", " + query_nature_of_judgement_select
                column_string += ", nature"


        if (not (query_judgement_select == "")):
            table_string = "Cases"
            if(value_string==""):
                value_string = query_judgement_select
                column_string= "judgement"
            else:
                value_string += ", " + query_judgement_select
                column_string += ", judgement"

        insert_query = "insert into " + table_string + "(" + column_string + ") values(" + value_string + ")"
        print(insert_query)

        cur = mysql.connection.cursor()
        row = cur.execute(insert_query)

        mysql.connection.commit()
        cur.close()

    return render_template('insert.html')


@app.route('/update.html', methods=['GET', 'POST'])



def index_update():
    rows = ","
    if request.method == "POST":
        details = request.form
        query_people_id_select = details['people_id']
        query_people_name_select = details['people_name']
        query_location_id_select = details['location_id']
        query_circuit_select = details['circuit']
        query_district_select = details['district']
        query_office_select = details['office']
        query_people_of_interest_id_select = details['people_of_interest_id']
        query_plaintiff_id_select = details['plaintiff_id']
        query_defendant_id_select = details['defendant_id']
        query_docket_number_select = details['docket_number']
        query_case_name_select = details['case_name']
        query_filing_date_select = details['filing_date']
        query_termination_date_select = details['termination_date']
        query_disposition_select = details['disposition']
        query_nature_of_judgement_select = details['nature_of_judgement']
        query_judgement_select = details['judgement']


        query_people_id_select2 = details['people_id2']
        query_people_name_select2 = details['people_name2']
        query_location_id_select2 = details['location_id2']
        query_circuit_select2 = details['circuit2']
        query_district_select2 = details['district2']
        query_office_select2 = details['office2']
        query_people_of_interest_id_select2 = details['people_of_interest_id2']
        query_plaintiff_id_select2 = details['plaintiff_id2']
        query_defendant_id_select2 = details['defendant_id2']
        query_docket_number_select2 = details['docket_number2']
        query_case_name_select2 = details['case_name2']
        query_filing_date_select2 = details['filing_date2']
        query_termination_date_select2 = details['termination_date2']
        query_disposition_select2 = details['disposition2']
        query_nature_of_judgement_select2 = details['nature_of_judgement2']
        query_judgement_select2 = details['judgement2']

        table_string = ""
        set_string = ""
        where_string = ""

        if (not (query_people_id_select == "")):
            table_string = "people"
            if(set_string==""):
                set_string = "people_id = " + query_people_id_select

            else:
                set_string += ", people_id = " + query_people_id_select


        if (not (query_people_name_select == "")):
            table_string = "people"
            if(set_string==""):
                set_string = "people_name = '" + query_people_name_select + "'"

            else:
                set_string += ", people_name = '" + query_people_name_select + "'"


        if (not (query_location_id_select == "")):
            table_string = "location"
            if(set_string==""):
                set_string = "location_id = " + query_location_id_select

            else:
                set_string += ", location = " + query_location_id_select


        if (not (query_circuit_select == "")):
            table_string = "location"
            if(set_string==""):
                set_string = "circuit = " + query_circuit_select

            else:
                set_string += ", circuit = " + query_circuit_select


        if (not (query_district_select == "")):
            table_string = "location"
            if(set_string==""):
                set_string = "district = " + query_district_select

            else:
                set_string += ", district = " + query_district_select

        if (not (query_office_select == "")):
            table_string = "location"
            if(set_string==""):
                set_string = "office = " + query_office_select

            else:
                set_string += ", office = " + query_office_select


        if (not (query_people_of_interest_id_select == "")):
            table_string = "people_of_interest"
            if(set_string==""):
                set_string = "people_of_interest_id = " + query_people_of_interest_id_select
            else:
                set_string += ", people_of_interest_id = " + query_people_of_interest_id_select

        if (not (query_plaintiff_id_select == "")):
            table_string = "people_of_interest"
            if(set_string==""):
                set_string = "plaintiff_id = " + query_plaintiff_id_select
            else:
                set_string += ", plaintiff_id = " + query_plaintiff_id_select



        if (not (query_defendant_id_select == "")):
            table_string = "people_of_interest"
            if(set_string==""):
                set_string = "defendant_id = " + query_defendant_id_select
            else:
                set_string += ", defendant_id = " + query_defendant_id_select

        if (not (query_docket_number_select == "")):
            table_string = "Cases"
            if(set_string==""):
                set_string = "docket_number = " + query_docket_number_select
            else:
                set_string += ", docket_number = " + query_docket_number_select


        if (not (query_case_name_select == "")):
            table_string = "Cases"
            if(set_string==""):
                set_string = "case_name = '" + query_case_name_select + "'"
            else:
                set_string += ", case_name = '" + query_case_name_select + "'"



        if (not (query_filing_date_select == "")):
            table_string = "Cases"
            if(set_string==""):
                set_string = "filing_date = '" + query_filing_date_select + "'"
            else:
                set_string += ", filing_date = '" + query_filing_date_select + "'"


        if (not (query_termination_date_select == "")):
            table_string = "Cases"
            if(set_string==""):
                set_string = "termination_date = '" + query_termination_date_select + "'"
            else:
                set_string += ", termination_date = '" + query_termination_date_select + "'"


        if (not (query_disposition_select == "")):
            table_string = "Cases"
            if(set_string==""):
                set_string = "disposition = " + query_disposition_select
            else:
                set_string += ", disposition = " + query_disposition_select


        if (not (query_nature_of_judgement_select == "")):
            table_string = "Cases"
            if(set_string==""):
                set_string = "nature = " + query_nature_of_judgement_select
            else:
                set_string += ", nature = " + query_nature_of_judgement_select

        if (not (query_judgement_select == "")):
            table_string = "Cases"
            if(set_string==""):
                set_string = "judgement = " + query_judgement_select
            else:
                set_string += ", judgement = " + query_judgement_select








        if (not (query_people_id_select2 == "")):
            if(where_string==""):
                where_string = "people_id = " + query_people_id_select2
            else:
                where_string += " and people_id = " + query_people_id_select2


        if (not (query_people_name_select2 == "")):
            if(where_string==""):
                where_string = "people_name = '" + query_people_name_select2 + "'"
            else:
                where_string += " and people_name = '" + query_people_name_select2 + "'"


        if (not (query_location_id_select2 == "")):
            if(where_string==""):
                where_string = "location_id = " + query_location_id_select2
            else:
                where_string += " and location_id = " + query_location_id_select2


        if (not (query_circuit_select2 == "")):
            if(where_string==""):
                where_string = "circuit = " + query_circuit_select2
            else:
                where_string += " and circuit = " + query_circuit_select2


        if (not (query_district_select2 == "")):
            if(where_string==""):
                where_string = "district = " + query_district_select2
            else:
                where_string += " and district = " + query_district_select2

        if (not (query_office_select2 == "")):
            if(where_string==""):
                where_string = "office = " + query_office_select2
            else:
                where_string += " and office = " + query_office_select2


        if (not (query_people_of_interest_id_select2 == "")):
            if(where_string==""):
                where_string = "people_of_interest_id = " + query_people_of_interest_id_select2
            else:
                where_string += " and people_of_interest_id = " + query_people_of_interest_id_select2



        if (not (query_plaintiff_id_select2 == "")):
            if(where_string==""):
                where_string = "plaintiff_id = " + query_plaintiff_id_select2
            else:
                where_string += " and plaintiff_id = " + query_plaintiff_id_select2



        if (not (query_defendant_id_select2 == "")):
            if(where_string==""):
                where_string = "defendant_id = " + query_defendant_id_select2
            else:
                where_string += " and defendant_id = " + query_defendant_id_select2

        if (not (query_docket_number_select2 == "")):
            if(where_string==""):
                where_string = "docket_number = " + query_docket_number_select2
            else:
                where_string += " and docket_number = " + query_docket_number_select2


        if (not (query_case_name_select2 == "")):
            if(where_string==""):
                where_string = "case_name = '" + query_case_name_select2 + "'"
            else:
                where_string += " and case_name = '" + query_case_name_select2 + "'"



        if (not (query_filing_date_select2 == "")):
            if(where_string==""):
                where_string = "filing_date = '" + query_filing_date_select2 + "'"
            else:
                where_string += " and filing_date = '" + query_filing_date_select2 + "'"


        if (not (query_termination_date_select2 == "")):
            if(where_string==""):
                where_string = "termination_date = '" + query_termination_date_select2 + "'"
            else:
                where_string += " and termination_date = '" + query_termination_date_select2 + "'"


        if (not (query_disposition_select2 == "")):
            if(where_string==""):
                where_string = "disposition = " + query_disposition_select2
            else:
                where_string += " and disposition = " + query_disposition_select2


        if (not (query_nature_of_judgement_select2 == "")):
            if(where_string==""):
                where_string = "nature = " + query_nature_of_judgement_select2
            else:
                where_string += " and nature = " + query_nature_of_judgement_select2

        if (not (query_judgement_select2 == "")):
            if(where_string==""):
                where_string = "judgement = " + query_judgement_select2
            else:
                where_string += " and judgement = " + query_judgement_select2


        update_query = "update " + table_string + " set " + set_string + " where " + where_string
        print(update_query)

        cur = mysql.connection.cursor()
        row = cur.execute(update_query)

        mysql.connection.commit()
        cur.close()

    return render_template('update.html')






@app.route('/query.html', methods=['GET', 'POST'])

def index_select():
    rows = ","
    df = pd.DataFrame()
    if request.method == "POST":
        details = request.form
        query_people_id_select = details['people_id']
        query_people_name_select = details['people_name']
        query_location_id_select = details['location_id']
        query_circuit_select = details['circuit']
        query_district_select = details['district']
        query_office_select = details['office']
        query_people_of_interest_id_select = details['people_of_interest_id']
        query_plaintiff_id_select = details['plaintiff_id']

        query_defendant_id_select = details['defendant_id']
        query_docket_number_select = details['docket_number']
        query_case_name_select = details['case_name']
        query_filing_date_select = details['filing_date']
        query_termination_date_select = details['termination_date']
        query_disposition_select = details['disposition']
        query_nature_of_judgement_select = details['nature_of_judgement']
        query_judgement_select = details['judgement']

        tables = []
        wheres = []
        table_string = ""
        where_string = ""

        if (not (query_people_id_select == "")):
            if "people" not in tables:
                tables.append("people")
            wheres.append("people_id = " + query_people_id_select)

        if (not (query_people_name_select == "")):
            if "people" not in tables:
                tables.append("people")
            wheres.append("people_name = '" + query_people_name_select + "'")

        if (not (query_location_id_select == "")):
            if "location" not in tables:
                tables.append("location")
            wheres.append("location_id = " + query_location_id_select)

        if (not (query_circuit_select == "")):
            if "location" not in tables:
                tables.append("location")
            wheres.append("circuit = " + query_circuit_select)

        if (not (query_district_select == "")):
            if "location" not in tables:
                tables.append("location")
            wheres.append("district = " + query_district_select)

        if (not (query_office_select == "")):
            if "location" not in tables:
                tables.append("location")
            wheres.append("office = " + query_office_select)

        if (not (query_people_of_interest_id_select == "")):
            if "people_of_interest" not in tables:
                tables.append("people_of_interest")
            wheres.append("people_of_interest_id = " + query_people_of_interest_id_select)

        if (not (query_plaintiff_id_select == "")):
            if "people_of_interest" not in tables:
                tables.append("people_of_interest")
            wheres.append("plaintiff_id = " + query_plaintiff_id_select)

        if (not (query_defendant_id_select == "")):
            if "people_of_interest" not in tables:
                tables.append("people_of_interest")
            wheres.append("defendant_id = " + query_defendant_id_select)

        if (not (query_docket_number_select == "")):
            if "Cases" not in tables:
                tables.append("Cases")
            wheres.append("docket_number = " + query_docket_number_select)

        if (not (query_case_name_select == "")):
            if "Cases" not in tables:
                tables.append("Cases")
            wheres.append("case_name = '" + query_case_name_select + "'")

        if (not (query_filing_date_select == "")):
            if "Cases" not in tables:
                tables.append("Cases")
            wheres.append("filing_date = '" + query_filing_date_select + "'")

        if (not (query_termination_date_select == "")):
            if "Cases" not in tables:
                tables.append("Cases")
            wheres.append("termination_date = '" + query_termination_date_select + "'")

        if (not (query_disposition_select == "")):
            if "Cases" not in tables:
                tables.append("Cases")
            wheres.append("disposition = " + query_disposition_select)

        if (not (query_nature_of_judgement_select == "")):
            if "Cases" not in tables:
                tables.append("Cases")
            wheres.append("nature_of_judgement = " + query_nature_of_judgement_select)


        if (not (query_judgement_select == "")):
            if "Cases" not in tables:
                tables.append("Cases")
            wheres.append("judgement = " + query_judgement_select)


        for table in tables:
            if table_string != "":
                table_string += " natural join " + table
            else:
                table_string = table

        for where in wheres:
            if where_string != "":
                where_string += " and " + where
            else:
                where_string = where

        select_query = "select * from " + table_string + " where " + where_string
        print(select_query)
        cur = mysql.connection.cursor()
        row = cur.execute(select_query)


        rows = cur.fetchall()
        for row in rows:
            print(row)
        mysql.connection.commit()

        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        if "people_of_interest_id" in field_names:
            i = field_names.index("people_of_interest_id")
            field_names[i] = "poi_id"

        cur.close()
        df = pd.DataFrame(rows, columns = field_names)

    return render_template('query.html', output = rows, tables=[df.to_html(classes='data', header="false")])


@app.route('/existing.html', methods=['GET', 'POST'])
# @app.route('/index/')
# @app.route('/index/<name>')

def index_existing():
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

    return render_template('existing.html',output = rows)

@app.route('/ai.html', methods=['GET', 'POST'])

def index_ai():
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
    winner = ""
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

        if((details['district'] == "") and (details['office'] == "") and (details['county'] == "") and (details['demanded'] == "") and (details['juris'] == "") and (details['origin'] == "") and (details['residenc'] == "") and (details['nos'] == "") and (details['section'] == "") and (details['county'] == "")):
            a = "All fields empty!"
        else:
            a = clf_gini.predict([test_case])
        print(a)


        if(a[0] == 1):
            winner = "Plaintiff will Win"
        if(a[0] == 2):
            winner = "Defendant will Win"
        if(a[0] == 3):
            winner = "Both will Win"

    return render_template('ai.html', output = winner)



if __name__ == '__main__':
    app.run(debug=True)
