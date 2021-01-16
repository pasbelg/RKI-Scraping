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

states = [u'Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
startDate = date(2020, 3, 4)
#startDate = date(2020, 8, 1)
endDate = date(2020, 12, 20)
#endDate = date(2020, 8, 11)
days = (endDate - startDate).days+1
urlSwitchDate = date(2020, 9, 1)
delta = timedelta(days=1)
runtimeExceptions = []
presentData = []
pastData = []
errorFile = open("files/out/scrapingErrors.txt", "w+", encoding="UTF8")
uncertainDataFile = open("files/out/manualValidation.txt", "w+", encoding="UTF8")
validDataFile = open("files/out/importableData.txt", "w+", encoding="UTF8")
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
#   Fälle und Todesfälle sind nicht gleichgroß/höher oder kein Vergleich möglich (z.B. Fehler in den Vergangenen Daten). Aus den Daten wird ein String gebildet und zu uncertain hinzugefügt. 
#   Das Bundesland ist nicht vorhanden. Aus dem Bundesland wird eine Fehlermeldung gebildet und als errors.
def checkIntegrity(states, pastData, presentData):
    valid = []
    uncertain = []
    errors = []
    dataString = ''
    presentValue = ''
    extractedData = ['Fälle', 'Todesfälle']
    for state in states:
        integrity = True
        if state in presentData:
            dateValue = presentData[presentData.index(state)+3]
            dataString = '(' + str(state) + ','
            for instance in extractedData:
                presentValue = presentData[presentData.index(state)+extractedData.index(instance)+1]
                if state in pastData:
                        pastValue = presentData[pastData.index(state)+extractedData.index(instance)+1]
                        if type(presentValue) == int and presentValue >= pastValue:
                            dataString = dataString + str(presentValue) + ','
                        else:
                            integrity = False
                            dataString = dataString + str(presentValue) + ','
                            integrityProblem = state + ' am ' + dateValue + ': ' + instance + ' sind niedriger als am Vortag'
                else:
                    integrity = False
                    dataString = dataString + str(presentValue) + ','
                    integrityProblem = state + ' am ' + dateValue + ': Kein Vergleich mit Vortag möglich'
            dataString = dataString + dateValue + ')'  
        else:
            errors.append(state + ' nicht gefunden')
            continue
        if integrity == True:
            valid.append(dataString)
        else:
            uncertain.append(dataString + ' ----- ' + integrityProblem)
    integrityIndex = {'validData':valid, 'uncertainData':uncertain, 'errors':errors}
    return integrityIndex

# Funktion die anhand des Datums den Link zum RKI und Rahmendaten wie die Position der Totesfälle in der Tabelle ermittelt und zurück gibt
def genSiteInfo(day):
    result = {'url':'', 'deathsColumn':''}
    urlID = day.strftime("%Y-%m-%d")
    urlPath = day.strftime("%b_%Y")
    if "Sep" in urlPath:
        urlPath = urlPath.replace("Sep", "Sept")
    if  day < urlSwitchDate:
        #alte URL (Tbl Seite 2) https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/2020-05-22-de.pdf?__blob=publicationFile
        result['url'] = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/'+urlID+'-de.pdf?__blob=publicationFile'
        page = 1
        result['deathsColumn'] = 4
        indexDeaths = 4
    else:
        #Neue URL & anderes PDf Format (Tbl Seite 4) https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Dez_2020/2020-12-08-de.pdf?__blob=publicationFile
        result['url'] = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/'+urlPath+'/'+urlID+'-de.pdf?__blob=publicationFile'
        page = 3
        result['deathsColumn'] = 6
        #indexDeaths = 6
    return result

# Funktion die fest definierte Zeichen aus einem Text entfernt und eine gesäuberte (leere String entfernt) Liste aller Wörter (ahnhand der Leerzeichen getrennt) zurück gibt.
def cleanText(text):
    charsToRemove = ['*', '.', '+', ' - ']
    for char in charsToRemove:
        text = text.replace(char, '')
    #Umwandeln des Textes in eine Liste (Leerzeichen sind Trenner)
    wordList = text.split(" ")
    #Alle '' aus der liste entfernen
    wordList = list(filter(None, wordList))
    return wordList

# Funktion um die gescrapten Daten nach der Überprüfung und Einordnung in die jeweilige Datei zu schreiben.
# Wird nur ein einzelner Wert übergeben, wird die URL zu den Laufzeitfehlern hinzugefügt und in die Fehler Datei geschrieben. 
def fileHandler(writeData, url, runtimeExceptions):
    if isinstance(writeData, dict):
        if len(writeData['errors']) != 0:
            if url not in runtimeExceptions:
                errorFile.write(url+'\n')
                for error in writeData['errors']:
                    errorFile.write(error+'\n')
        for data in writeData['validData']:
            validDataFile.write(data+'\n')
        if len(writeData['uncertainData']) != 0:
            for data in writeData['uncertainData']:
                uncertainDataFile.write(data+'\n')
    else:
        if url not in runtimeExceptions:
            runtimeExceptions.append(url)
            errorFile.write(url+'\n')
            errorFile.write(str(writeData)+'\n')
    return runtimeExceptions

# Funktion um die benötigten Daten aus der Liste der gesprapten Wörtern des PDFs zu ziehen und in einer Liste zu speichern.
def getRelvantData(wordList, day, indexCases, indexDeaths):
    #Hinzufügen des Bundeslands
    result.append(wordList[stateCell])
    #Hinzufügen der Corona Fälle (die Fälle sind immer der erste Wert nach dem Bundesland)
    result.append(int(wordList[stateCell+indexCases]))
    #Am Anfang wurden noch keine Todesfälle angegeben. Erst ab 17.03.2020 sind Todesfälle enthalten
    if day < date(2020, 3, 17):
        #Hinzufügen der Corona Todesfälle als 0 weil sie noch nicht in den Daten vorhanden sind
        result.append(0)
    else:
        #Hinzufügen der Corona Todesfälle (die Position der Todesfälle wurde in genSiteInfo anhand des Datums ermittelt)
        result.append(int(wordList[stateCell+indexDeaths]))
    #Hinzufügen des Datums
    result.append(day.strftime("%Y-%m-%d"))

while startDate <= endDate:
    result = []
    curDate = startDate
    siteData = genSiteInfo(curDate)
    url = siteData['url']
    response = requests.get(url, headers=header)
    print(url)
    try:
        with io.BytesIO(response.content) as open_pdf_file:
            pdfText = getTable(open_pdf_file, states)
            wordList = cleanText(pdfText)
            dataCount = 0
            for state in states:
                stateCell = getCorrectIndex(wordList, state)
                if stateCell == False:
                    continue
                else:
                    getRelvantData(wordList, curDate, 1, siteData['deathsColumn'])
                    #Es werden immer 4 Einzeldaten hinzugefügt.Deswegen wir der Zähler für die spätere Validierung um 4 erhöht. Bei Fehlenden Daten greift die Exeption also auch kein Zähler.
                    dataCount = dataCount + 4
    except Exception as e:
        error = 'Fehler beim Scraping: ' + str(e)
        runtimeExceptions = fileHandler(error, url, runtimeExceptions)
        pass
    try:
        presentData = result[len(result)-dataCount:len(result)]
        integrityIndex = checkIntegrity(states, pastData, presentData)
        fileHandler(integrityIndex, url, runtimeExceptions)
        pastData = result[len(result)-dataCount:len(result)]
    except Exception as e:
        error = 'Fehler beim schreiben der Daten: ' + str(e)
        runtimeExceptions = fileHandler(error, url, runtimeExceptions)
        pass
    startDate += delta

errorFile.close()
uncertainDataFile.close()
validDataFile.close()