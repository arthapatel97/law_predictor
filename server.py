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
    g = "bro"
    rows = ","
    if request.method == "POST":

        details = request.form
        query1 = details['docket_number']
        query2 = details['people_id']
        query3 = details['location_id']
        # mycursor = mydb.cursor()

        # sql = "INSERT IGNORE INTO people (people_id, people_name) VALUES (%s, %s)"
        # val = (500, "wild")
        # mycursor.execute(sql, val)

        # mycursor.execute(query)
        # mydb.commit()


        cur = mysql.connection.cursor()
        if(not (query1 == "")):
            row = cur.execute("select * from Cases where docket_number = " + query1)
        if(not (query2 == "")):
            row = cur.execute("select * from people where people_id = " + query2)
        if(not (query3 == "")):
            row = cur.execute("select * from location where location_id = " + query3)
        # row = cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        mysql.connection.commit()
        cur.close()
        # print(query)
    return render_template('index.html',output = rows[0])

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
