import mysql.connector
import requests
from bs4 import BeautifulSoup
import random
import warnings
warnings.filterwarnings("ignore")

nums = random.sample(range(1000000,3000000), 5000)

mydb = mysql.connector.connect(user='root', password='password',
                              host='localhost',
                              database='Case_record')

case_id = 50
person_id = 50
person_id2 = 51
people_of_interest_id = 1
location_id = 100


for j in range(len(nums)):
    URL = "https://www.fjc.gov/research/idb/interactive/detail/IDB-civil-since-1988/" + str(nums[j]) + "?width=650&height=800"
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
    print(j)
    for row in rows:
        dataobj = row.find("td")

        toprint = dataobj.text.strip()
        arr.append(toprint)

    plaintiff = arr[21]
    defendant = arr[22]
    circuit = int(arr[0])
    district = arr[1]
    office = int(arr[2])
    docket_num = int(arr[3])
    filing_date = arr[5]
    termination_date = arr[27]
    disposition = int(arr[33])
    natureofjudgement = int(arr[34])
    judgement = int(arr[36])

    JURIS = arr[7]
    NOS= arr[8]
    SECTION = arr[10]
    DISTRICT= arr[1]
    ORIGIN = arr[4]
    DOCKET = arr[3]
    RESIDENC = arr[12]
    TAPEYEAR = arr[45]
    FILEDATE = arr[5]
    PLT = arr[21]
    TDATEUSE= arr[28]
    OFFICE= arr[2]
    DEMANDED= arr[15]
    COUNTY= arr[18]
    JUDGEMENT = arr[36]



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


    sql = "INSERT IGNORE INTO Cases (docket_number, location_id, case_name, filing_date, termination_date, disposition, nature, judgement, people_of_interest_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (docket_num, location_id, case_name, filing_date, termination_date, disposition, natureofjudgement, judgement,people_of_interest_id)
    mycursor.execute(sql, val)

    sql = "INSERT IGNORE INTO training_model (juris, nos, section, district, origin, docket, residenc, tapeyear, filedate, plt, tdateuse, office, demanded, county, judgement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (JURIS, NOS, SECTION, DISTRICT, ORIGIN, DOCKET, RESIDENC, TAPEYEAR, FILEDATE, PLT, TDATEUSE, OFFICE, DEMANDED, COUNTY, JUDGEMENT)
    mycursor.execute(sql, val)


    mydb.commit()
    person_id += 2
    person_id2 += 2
    location_id += 1
    people_of_interest_id += 1
