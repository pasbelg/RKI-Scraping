# Import um das Programm abzubrechen
import sys

def qmCalc(lenght, width):
    # Prüfen ob Länge und Breite valide sind (größer als 0)
    # Prüfen ob Länge valide ist
    if lenght <= 0:
        print('Bitte geben sie eine valide Länge ein')
    # Prüfen ob Breite valide ist
    elif width <= 0:
        print('Bitte geben Sie eine valide Breite ein')
    # Ist alles valide wird die Berechnung durchgeführt und die
    else:
        qm = lenght * width
        return qm 

def stringToFloat(string):
    # Jedes Wort (Leerzeichen wird als Trennzeichen geutzt) wird einzeln durchgegangen
    for word in string.split():
        # Wenn das erste Zeichen im Wort eine Zahl ist
        if word[0].isdigit():
            # Wenn im Wort ein Komma enthalten ist wird es in einen Punk umgewandelt damit es zu einem float werden kann
            if "," in word:
                word = word.replace(",", ".")    
        #Es wird versucht das Wort in eine Fließkommazahl umzuwandeln
        try:
            return float(word)
        #Ist dies nicht möglich wird eine Fehlermeldung ausgegeben und das Programm beendet
        except:
            sys.exit("Bitte geben überprüfen Sie ihre Eingabe!")

# Länge abfragen
lenght = input('Geben Sie die Länge des Raums ein:\n')
# Länge in zahl umwandeln
lenght = stringToFloat(lenght)
# Breite abfragen
width = input('Geben Sie die Breite des Raums ein:\n')
# Breite in zahl umwandeln
width = stringToFloat(width)

qm = qmCalc(lenght, width)
print('Der Raum hat', qm, 'Quadratmeter')