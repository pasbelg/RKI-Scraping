import pandas as pd
import requests
from datetime import datetime
import unicodedata

import mysql.connector
def conDB():
    #DB Config
    mydb= mysql.connector.connect(
        host="localhost",
        user="root",
        password="toor",
        database="coronaDaly"
    )
    return mydb
#DB Verbindung herstellen
try:
    db = conDB()
    print('Aufbau der Verbindung wird gestartet.')
    print('Datenbankverbindung erfolgreich hergestellt.')
except Exception as e:
    print('Aufbau der Verbindung wird gestartet.')
    print('Datenbankverbindung gescheitert')
    print(e)
mycursor = db.cursor()
def getStateID(state):
  sql = 'SELECT ID FROM states where Bundesland = "'+state+'"'
  mycursor.execute(sql)
  return mycursor.fetchall()

#Funktion um einen Task inkl. Priorität in der Datenbank anzulegen
def insertData(tablename, data):
    sql = 'INSERT INTO '
    if tablename == 'states':
      sql = sql + 'states (Bundesland) select "'+data+'" WHERE NOT EXISTS (SELECT * FROM states WHERE Bundesland = "'+data+'");'  
    elif tablename == 'cases':
      print(data)
      sql = sql + 'cases (ID, bundeslandID, anzahl, tote, date) select "'+data+'" WHERE NOT EXISTS (SELECT * FROM cases WHERE date != CURDATE());'
    else:
      return 0 
    mycursor.execute(sql)
    db.commit()
    print('Datensatz (' + data + ') angelegt') 

site= "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
hdr = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

req = requests.get(site, headers=hdr)
#HTML säubern da Pandas die Punkte in den Zahlen sonst als Komma ansieht
html = req.text.replace('.', '')
coronaDataRKI = pd.read_html(html)
coronaDataRKI = coronaDataRKI[0]
coronaDataRKI.columns=['Bundes­land', 'An­zahl', 'Dif­fe­renz zum Vor­tag', 'Fälle in den letzten 7 Tagen', '7-Tage-Inzidenz', 'Tote']
coronaDataRKI = coronaDataRKI.drop(['Dif­fe­renz zum Vor­tag', 'Fälle in den letzten 7 Tagen', '7-Tage-Inzidenz'], axis=1)
coronaDataRKI = coronaDataRKI.replace('[^A-Za-z0-9äÄöÖüÜß-]+', '', regex=True)
#coronaDataRKI['Tote'] = coronaDataRKI['Tote'].astype('int')
print(coronaDataRKI)
states = coronaDataRKI['Bundes­land'].values.tolist()
cases = coronaDataRKI.to_records(index=False)
for bundesland in states:
  insertData('states', str(bundesland))
for case in cases:
  stateID = getStateID(case[0])[0][0]
  case[0] = stateID
  insertData('cases', str(case))

#for bundesland in liste:
#  insertData('states', states)