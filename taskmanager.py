import mysql.connector
def conDB():
    #DB Config
    mydb= mysql.connector.connect(
        host="localhost",
        user="root",
        password="toor",
        database="taskmanager"
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

#Funktion um alle Tasks aus der Datenbank auszugeben
def getTasks():
    sql = "SELECT * FROM tasks"
    mycursor.execute(sql)
    tasks = mycursor.fetchall()
    return tasks

#Funktion um einen bestimmten Task aus der Datenbank zu löschen (Leider gibt execute keinen Fehler aus wenn kein Datensatz gefunden wurde sonst hätte ich das mit try gemacht)
def delTask(task):
    for data in getTasks():
        if task in data:
            ID = str(data[0])
            print('Task '+task+' mit ID '+str(data[0])+' gelöscht.')
            #Es wird immer nur der 1. Datensatz mit dem task gelöscht. Falls es mehrere gibt muss das Progamm erneut ausgeführt werden.
            sql = 'DELETE FROM tasks WHERE task = "'+task+'" AND idtasks = "'+ID+'"'
            mycursor.execute(sql)
            db.commit()
            #Funktion abbrechen, weil jetzt der älteste Datensatz gelöscht wurde
            return
        else:
            # Speichern der Fehlermeldung wenn Task nicht in DB gefunden wurde
            error = 'Task nicht gefunden, überprüfen Sie ihre Eingabe.\nIhre Eingabe: '+task+'\nTasks in der Datenbank:'

    # Ausgabe des Fehlers außerhalb der Schleife (mit try falls error nicht gefüllt ist)
    try:
        print(error)
    except:
        pass
    #Ausgabe des Inhalts der Datenbank
    for data in getTasks():
        print(data)

#Funktion um einen Task inkl. Priorität in der Datenbank anzulegen
def insertTask(task, prio):
    sql = 'INSERT INTO tasks (idtasks, task, prio) VALUES (NULL, "'+task+'", '+str(prio)+')'
    mycursor.execute(sql)
    db.commit()
    print('Task '+task+' mit Priorität '+prio+' angelegt') 

#Frontend
wahl = input('Was möchten Sie tun? (1=Tasks ansehen, 2=Tasks anlegen, 3=Tasks löschen): ')
if (wahl == '1'):
    for task in getTasks():
        print(task)
elif(wahl == '2'):
    task = input('Bitte einen neuen Task eingeben: ')
    prio = input('Jetzt noch die Priorität des Tasks: ')
    try:
        insertTask(task, prio)
    except:
        print('Falsche eingabe')
elif(wahl == '3'):
    task = input('Bitte einen vorhanden Task eingeben (Falls mehrere Tasks mit diesem Namen existieren wird nur der älteste gelöscht): ')
    try:
        delTask(task)
    except:
        print('Falsche eingabe')
else:
    print('Keine gültige wahl getroffen')