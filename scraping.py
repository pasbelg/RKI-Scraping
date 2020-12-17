import pandas as pd

#Import für Aufgabe 3 (Richtiges Zeitformat)
import locale
locale.setlocale(locale.LC_ALL, "german")
#Importe für RKI Scraping
import requests


# Aufgabe 1
uriAPI="https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?waters=RHEIN,MAIN"
pegel = pd.read_json(uriAPI)

# Aufgabe 2
uri="https://www.rnd.de/gesundheit/corona-zahlen-aktueller-stand-am-09122020-karten-grafiken-informationen-ZF7G5L2KOREUFDX5XF4HGGXDFI.html"
coronaRND = pd.read_html(uri)[0]
coronaRND.columns=['Ort', 'Infektionen', 'Todesfälle', 'Genesungen', 'Bevölkerung']
coronaRND.to_excel("files/out/CoronaRND.xlsx")

# Zusatzaufgabe
path = "files/in/coronaDeutschlandStatista.xlsx"
coronaDataStatista = pd.read_excel(path, sheet_name='Daten')
coronaDataStatista = coronaDataStatista[4:len(coronaDataStatista)]
coronaDataStatista.columns=['löschen', 'Datum', 'Infektionen', 'Tote']
coronaDataStatista = coronaDataStatista.drop(['löschen'], axis=1)
coronaDataStatista = coronaDataStatista.replace('[^A-Za-z0-9äÄöÖüÜß]+', '', regex=True)
coronaDataStatista['Datum'] = coronaDataStatista['Datum'].astype(str)+'2020'
coronaDataStatista['Datum'] = pd.to_datetime(coronaDataStatista['Datum'], format='%d%b%Y', errors='coerce' ) 
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(coronaDataStatista)
index = coronaDataStatista['Datum']
data = coronaDataStatista['Infektionen']
s = pd.Series(data, index)
s.plot()


#Entwurf eines Scrapers für die aktuellen RKI-Corona Daten
site= "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
hdr = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

req = requests.get(site, headers=hdr)
coronaDataRKI = pd.read_html(req.text)
coronaDataRKI = coronaDataRKI[0]
coronaDataRKI.columns=['Bundes­land', 'An­zahl', 'Dif­fe­renz zum Vor­tag', 'Fälle in den letzten 7 Tagen', '7-Tage-Inzidenz', 'Todesfälle']