key = 20
f = open('files/in/nachricht.txt','r')
text = f.read()
f.close()
chiffre = ''
klartext = ''
def cryptChar(char, key, decrypt):
    #Wenn decrypt mit als wahr übergeben wurde soll entschlüsselt werden
    if decrypt:
        #Entschlüsselung mit Modulo 27 (da 27 Zeichen in der Liste)
        return str(chr(ord(zeichen)-key%1114111))
    else:
        #Verschlüsselung mit Modulo 27 (da 27 Zeichen in der Liste)
        return str(chr(ord(zeichen)+key%1114111))

for zeichen in text:
    chiffre = chiffre + cryptChar(zeichen, key, False)
f = open('files/out/chiffre.txt','w')
f.write(chiffre)
f.close()
f = open('files/out/chiffre.txt','r')
chiffre = f.read()
for zeichen in chiffre:
    klartext = klartext + cryptChar(zeichen, key, True)
print(klartext)