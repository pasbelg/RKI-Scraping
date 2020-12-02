liste = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ']
#Für das Umlaut-Problem macht es wahrscheinlich mehr Sinn die Buchstabenliste zu erweitern und das Modulo anzupassen
umlaute = {'Ä' : 'AE', 'Ö' : 'OE', 'Ü' : 'UE'}
key = 5
text = input("Bitte geben Sie den Text ein den Sie verschlüsseln wollen: ")
#Leere Variablen deklarieren damit diese gefüllt werden können
chiffre = ''
klartext = ''
def replaceUmlaut(char):
    for umlaut, replacement in umlaute.items():
        if char == umlaut:
            return char.replace(char, replacement)
        #Muss noch optimiert werden, weil sonst Wörter mit z.B. AE wie Aerodynamik in Ärodynamik umgewandelt würden
        elif char == replacement:
            return char.replace(char, umlaut)
    return char

def crypt(char, key, decrypt):
    #Zähler zum durchlaufen der Liste
    i=0  
    for zeichen in liste:
        if char == zeichen:
            #Wenn decrypt mit als wahr übergeben wurde soll entschlüsselt werden
            if decrypt:
                #Entschlüsselung mit Modulo 27 (da 27 Zeichen in der Liste)
                return liste[(i-key)%27]    
            else:
                #Verschlüsselung mit Modulo 27 (da 27 Zeichen in der Liste)
                return liste[(i+key)%27]
        i = i+1
    #Werde keine Buchstarben übergeben soll das gleiche Zeichen ausgegeben werden (nach der Schleife damit Leerzeichen nicht berücksichtigt werden)
    if not char.isalpha():
        return str(char)

for zeichen in text:
    zeichen = replaceUmlaut(zeichen.upper())
    #Weil jetzt AE, OE und UE jeweils 2 Zeichen sind nochmal eine Schleife durch alle Zeichen
    for einzelzeichen in zeichen:
        #Neue Zeichenkette mit den verschobenen Zeichen
        chiffre = chiffre + crypt(einzelzeichen, key, False)
print(chiffre)
for zeichen in chiffre:
    klartext = klartext + crypt(zeichen.upper(), key, True)
print(klartext)
