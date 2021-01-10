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
startDate = date(2020, 3, 4)
endDate = date(2020, 5, 10)
#endDate = date(2021, 1, 8)
days = (endDate - startDate).days+1
urlSwitchDate = date(2020, 9, 1)
delta = timedelta(days=1)
liste = []
# Funktion um Seite mit der gewünschten Tabelle zu ermitteln (Tabelle 1 kann leider in vielen PDFs nicht gefunden werden)
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
        if stateCount >= 12:
            return pdfText
    return 'keine Tabelle gefunden'   

# Funktion um die richtige Zelle zu ermitteln
# Wenn das Wort mehrmals gefunden wurde wird evaluiert, ob die übernächste Zelle eine Zahl ist. Wenn ja ist es dir richtige Zelle.
def getCorrectIndex(pdfList, word):

    wordOccurence = pdfList.count(word)
    if wordOccurence == 1:
        return pdfList.index(word)
    #Fall um richitge Stelle für Bundesland und Todesfälle zu ermitteln
    elif wordOccurence > 1:
        indices = [i for i, x in enumerate(pdfList) if x == word]
        #print(indices)
        for index in indices:
            #print(pdfList[index+2])
            if pdfList[index+1].isdigit():
                return index
    else:
        return False

# Funktion um die Integrität der Daten zu überprüfen.
# Es werden die erhobenen Daten aus den letzten zwei Tagen verglichen.
# Fallunterscheidung:
#   Fälle und Todesfälle sind gleichgroß/höher. Aus den Daten wird ein String gebildet und zu valid hinzugefügt. 
#   Fälle und Todesfälle sind nicht gleichgroß/höher oder kein Vergleich möglich (z.B. Fehler in den Vergangenen Daten). Aus den Daten wird ein String gebildet und zu unknown hinzugefügt. 
#   Das Bundesland ist nicht vorhanden. Aus dem Bundesland wird eine Fehlermeldung gebildet und als errors.
def checkIntegrity(states, pastData, presentData):
    valid = []
    unknown = []
    errors = []
    dataString = ''
    extractedData = ['Fälle', 'Todesfälle']
    for state in states:
        integrity = True
        if state in presentData:
            dateValue = presentData[presentData.index(state)+3]
            dataString = '(' + str(state) + ','
            if state in pastData:
                for instance in extractedData:
                    pastValue = presentData[pastData.index(state)+extractedData.index(instance)+1]
                    presentValue = presentData[presentData.index(state)+extractedData.index(instance)+1]
                    if presentValue >= pastValue:
                        dataString = dataString + str(presentValue) + ','
                    else:
                        integrity = False
                        dataString = dataString + str(presentValue) + ','
                        #errors.append('Falsche Daten in: ' + data + state)
            else:
                integrity = False
                dataString = dataString + str(presentValue) + ','
                #errors.append(state + ' kein Vergleich möglich')
            dataString = dataString + dateValue + ')'  
        else:
            errors.append(state + ' nicht Vorhanden')
        if integrity == True:
            valid.append(dataString)
        else:
            unknown.append(dataString)
    integrityIndex = {'validData':valid, 'unknownData':unknown, 'errors':errors}
    return integrityIndex

f = open("files/out/log.txt", "w+")
while startDate <= endDate:
    curDate = startDate
    urlID = curDate.strftime("%Y-%m-%d")
    urlPath = curDate.strftime("%b_%Y")
    if "Sep" in urlPath:
        urlPath = urlPath.replace("Sep", "Sept")
    if  curDate < urlSwitchDate:
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
    #f.write(url+'\n')
    try:
        with io.BytesIO(response.content) as open_pdf_file:
            pdfText = getTable(open_pdf_file, states)
            pdfText = pdfText.replace("*", "")
            pdfText = pdfText.replace(".", "")
            pdfText = pdfText.replace("+", "")
            pdfText = pdfText.replace(" - ", "")
            #Umwandeln des Textes in eine Liste (Leerzeichen sind Trenner)
            wordList = pdfText.split(" ")
            #Alle '' aus der liste entfernen
            wordList = list(filter(None, wordList))
            dataCount = 0
            for state in states:
                stateCell = getCorrectIndex(wordList, state)
                if stateCell == False:
                    f.write(url+'\n')
                    f.write('error at '+ state + '\n')
                    continue
                else:
                    liste.append(wordList[stateCell]); dataCount = dataCount + 1
                    liste.append(int(wordList[stateCell+1])); dataCount = dataCount + 1
                    #f.write('success at '+ state + '\n')
                    #f.write('Bundesland: ' + wordList[stateCell]+'\n')
                    #f.write('Anzahl: ' + wordList[stateCell+1]+'\n')
                    #Am Anfang wurden noch keine Todesfälle angegeben. Erst ab 17.03.2020 sind Todesfälle enthalten
                    if curDate < date(2020, 3, 17):
                        liste.append(0); dataCount = dataCount + 1
                    else:
                        liste.append(int(wordList[stateCell+deathsIndex])); dataCount = dataCount + 1
                        #f.write('Tote: ' + wordList[stateCell+deathsIndex]+'\n')
                    liste.append(urlID); dataCount = dataCount + 1
    except Exception as e:
        f.write('"'+url+'",\n')
        f.write(str(e)+'\n')
        print(e)
  
    presentData = liste[len(liste)-dataCount:len(liste)]
    try: 
        integrityIndex = checkIntegrity(states, pastData, presentData)
        if len(integrityIndex['errors']) != 0:
            f.write('"'+url+'",\n')
            for error in integrityIndex['errors']:
                f.write('"'+error+'",\n')
    except Exception as e:
        f.write('"'+url+'",\n')
        f.write(str(e)+'\n')
        print(e)
    pastData = liste[len(liste)-dataCount:len(liste)]

    startDate += delta

print(liste)
values = 4*16*days - 9*4
print(days)
print(len(liste))
fehler = values-len(liste)
print('Daten ohne Fehler:', len(liste), 'Erwartete Einträge:', values, 'Fehlende Daten insgesamt:', fehler)
f.write('Extrahierte Daten: '+ str(len(liste)) + ' Erwartete Einträge: ' + str(values) + ' Fehlende Daten insgesamt: '+ str(fehler))
f.close()
'''
response = requests.get(site, headers=header)
with io.BytesIO(response.content) as open_pdf_file:
    print(getTable(open_pdf_file))
'''