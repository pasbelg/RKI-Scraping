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
endDate = date(2020, 12, 10)
days = (endDate - startDate).days+1
switchDate = date(2020, 9, 1)
delta = timedelta(days=1)
liste = []
def getTable(pdf):
    #Funktion um die Seite/den Text aus dem PDF zu extrahieren auf dem der String Tabelle 1 zu finden ist
    #Hierfür muss jede Seite extrahiert werden und sobald Tabelle 1 gefunden wurde aus der Funktion returnt werden.
    pdfReader = PyPDF2.PdfFileReader(pdf)
    while counter < Seitengesamtanzahl:
        pageObj = pdfReader.getPage(counter)
        if "Tabelle 1" in pdfText:
            return pageObj.extractText()
        

f = open("files/out/log.txt", "a")
while startDate <= endDate:
    urlID = startDate.strftime("%Y-%m-%d")
    urlPath = startDate.strftime("%b_%Y")
    if "Sep" in urlPath:
        urlPath = urlPath.replace("Sep", "Sept")
    if  startDate < switchDate:
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
    f.write(url+'\n')
    print(url)
    try:
        with io.BytesIO(response.content) as open_pdf_file:
            pdfReader = PyPDF2.PdfFileReader(open_pdf_file)
            pageObj = pdfReader.getPage(page)
            pdfText = pageObj.extractText()
            pdfText = pdfText.replace("\n", "")
            pdfText = pdfText.replace("*", "")
            wordList = pdfText.split(" ")
            for state in states:
                firstCell = wordList.index("Baden-Württemberg")
                stateCell = wordList.index(state)
                liste.append(wordList[stateCell])
                liste.append(wordList[stateCell+1])
                #print(wordList[stateCell])
                #print(wordList[stateCell+1])
                if wordList[firstCell-1] == "Todesfälle" or wordList[firstCell-1] == "Einw.":
                    liste.append(wordList[stateCell+deathsIndex])
                    #print(wordList[stateCell+deathsIndex])
                else:
                    try:
                        f.write(str(wordList[stateCell])+'\n')
                        f.write(str(wordList[stateCell-1])+'\n')
                        f.write(str(wordList[stateCell+1])+'\n')
                    except:
                        pass
                    print('Fehler in', wordList[stateCell])
                   
    except Exception as e:
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
