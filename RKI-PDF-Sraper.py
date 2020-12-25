#link zu den pdfs: https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/2020-05-22-de.pdf?__blob=publicationFile
#Geht aber nur bis 2020-08-31
#Ab dann "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Dez_2020/2020-12-08-de.pdf?__blob=publicationFile" (da ist die Tabelle dann auf seite 4)
from datetime import date, timedelta
import requests, PyPDF2, io
import locale
locale.setlocale(locale.LC_ALL, "german")
site= "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/2020-05-22-de.pdf?__blob=publicationFile"
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

states = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
startDate = date(2020, 3, 10)
endDate = date(2020, 3, 10)
days = (endDate - startDate).days+1
urlSwitchDate = date(2020, 9, 1)
delta = timedelta(days=1)
liste = []
#Funktion um Seite mit der gewünschten Tabelle zu ermitteln (Tabelle 1 kann leider in vielen PDFs nicht gefunden werden)
def getTable(pdf, states):
    pdfReader = PyPDF2.PdfFileReader(pdf)
    pageCount = pdfReader.getNumPages()
    for page in range(0, pageCount):
        pageObj = pdfReader.getPage(page)
        pdfText = pageObj.extractText()
        pdfText = pdfText.replace("\n", "")
        stateCount = 0
        #Die Seite auf der mindestens 13 Bundesländer gefunden wurden ist sehr wahrscheinlich die mit der Tabelle
        for state in states:
            if state in pdfText:
                stateCount=stateCount+1
        if stateCount >= 13:
            return pdfText
    return 'keine Tabelle gefunden'

def getCorrectIndex(pdfList, state):
    #Funktion um die richtige Zelle zu ermitteln
    #Wenn das Bundesland mehrmals gefunden wurde muss evaluiert werden ob die nächste und vorige Zelle eine Zahl ist. Wenn ja ist es dir richtige Zelle.
    stateOccurence = pdfList.count(state)
    if stateOccurence == 1:
        return pdfList.index(state)
    elif stateOccurence > 1:
        indices = [i for i, x in enumerate(pdfList) if x == state]
        print(indices)
        for index in indices:
            print(pdfList[index+1])
            if pdfList[index+1].isdigit():
                return index
    else:
        return False

f = open("files/out/log.txt", "w+")
while startDate <= endDate:
    urlID = startDate.strftime("%Y-%m-%d")
    urlPath = startDate.strftime("%b_%Y")
    if "Sep" in urlPath:
        urlPath = urlPath.replace("Sep", "Sept")
    if  startDate < urlSwitchDate:
        #alte URL (Tbl Seite 2) https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/2020-05-22-de.pdf?__blob=publicationFile
        url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/'+urlID+'-de.pdf?__blob=publicationFile'
        page = 1
        deathsIndex = 4
    else:
        #Neue URL & anderes PDf Format (Tbl Seite 4) https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Dez_2020/2020-12-08-de.pdf?__blob=publicationFile
        url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/'+urlPath+'/'+urlID+'-de.pdf?__blob=publicationFile'
        page = 3
        deathsIndex = 6
    response = requests.get(url, headers=header)
    print(url)
    try:
        with io.BytesIO(response.content) as open_pdf_file:
            pdfText = getTable(open_pdf_file, states)
            pdfText = pdfText.replace("*", "")
            pdfText = pdfText.replace(".", "")
            #Umwandeln des Textes in eine Liste (Leerzeichen sind Trenner)
            wordList = pdfText.split(" ")
            #Alle '' aus der liste entfernen
            wordList = list(filter(None, wordList))

            for state in states:
                stateCell = getCorrectIndex(wordList, state)
                if stateCell == False:
                    continue
                else:
                    liste.append(wordList[stateCell])
                    liste.append(wordList[stateCell+1])
                    #Am Anfang wurden noch keine Todesfälle angegeben. Sobald das Wört "Todesfälle" enthalten ist und das führende und folgende Wort keine Zahl ist ist es in der tabelle
                    if 'Todesfälle' in wordList:
                        liste.append(wordList[stateCell+deathsIndex])
                    else:
                        liste.append(0)
                    #f.write('Bundesland: ' + wordList[stateCell]+'\n')
                    #f.write('Anzahl: ' + wordList[stateCell+1]+'\n')
                    #f.write('Tote: ' + wordList[stateCell+deathsIndex]+'\n')
    except Exception as e:
        f.write('"'+url+'",\n')
        f.write(str(e)+'\n')
        print(e)
    startDate += delta
f.close()
print(liste)
values = 3*16*days
print(days)
print(len(liste))
fehler = values-len(liste)
print('Daten ohne Fehler:', values, 'Fehlende Daten insgesamt:', fehler)
'''
response = requests.get(site, headers=header)
with io.BytesIO(response.content) as open_pdf_file:
    print(getTable(open_pdf_file))
'''