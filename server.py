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
def index1():
    if request.method == "POST":

        details = request.form
        query = details['statement']


        cur = mysql.connection.cursor()
        cur.execute(query)
        # store = cur.execute(query)
        # print(store)
        mysql.connection.commit()
        cur.close()
        print(query)
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
