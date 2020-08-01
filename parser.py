import mysql.connector
import requests
from bs4 import BeautifulSoup

mydb = mysql.connector.connect(user='root', password='password',
                              host='localhost',
                              database='Case_record')


entry_num = 40
case_id = 50
person_id = 50
person_id2 = 51
people_of_interest_id = 1
location_id = 100


for i in range(100):
    URL = "https://www.fjc.gov/research/idb/interactive/detail/IDB-civil-since-1988/" + str(entry_num) + "?width=650&height=800"
    page = requests.get(URL, verify=False)

    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("body")
    first = table.find("div")
    for i in range(5):
        first = first.find("div")

    first = first.findAll("div")[1]
    first = first.find("div")
    first = first.find("table")
    first = first.find("tbody")

    rows = first.findAll("tr")
    arr = []
    for row in rows:
        dataobj = row.find("td")

        toprint = dataobj.text.strip()
        arr.append(toprint)

    plaintiff = arr[21]
    defendant = arr[22]
    circuit = int(arr[0])
    district = int(arr[1])
    office = int(arr[2])
    docket_num = int(arr[3])
    filing_date = arr[5]
    termination_date = arr[27]
    disposition = int(arr[33])
    natureofjudgement = int(arr[34])
    judgement = int(arr[36])
    case_name = "Civil"

    mycursor = mydb.cursor()

    sql = "INSERT IGNORE INTO people (people_id, people_name) VALUES (%s, %s)"
    val = (person_id, plaintiff)
    mycursor.execute(sql, val)

    sql = "INSERT IGNORE INTO people (people_id, people_name) VALUES (%s, %s)"
    val = (person_id2, defendant)
    mycursor.execute(sql, val)

    sql = "INSERT IGNORE INTO location (location_id, circuit, district, office) VALUES (%s, %s, %s, %s)"
    val = (location_id, circuit, district, office)
    mycursor.execute(sql, val)

    sql = "INSERT IGNORE INTO people_of_interest (people_of_interest_id, plaintiff_id, defendant_id) VALUES (%s, %s, %s)"
    val = (people_of_interest_id, person_id, person_id2)
    mycursor.execute(sql, val)


    sql = "INSERT IGNORE INTO Cases (docket_number, location_id, case_name, filing_date, termination_date, disposition, nature, judgement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (docket_num, location_id, case_name, filing_date, termination_date, disposition, natureofjudgement, judgement)
    mycursor.execute(sql, val)

    mydb.commit()
    entry_num += 1
    person_id += 2
    person_id2 += 2
    location_id += 1
    people_of_interest_id += 1
