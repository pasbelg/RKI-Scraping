import mysql.connector
def conDB():
    #Verbindung herstellen
    mydb= mysql.connector.connect(
        host="localhost",
        user="root",
        password="toor",
        database="taskmanager"
    )
    return mydb
try:
    db = conDB()
    print('Aufbau der Verbindung wird gestartet.')
    print('Datenbankverbindung erfolgreich hergestellt.')
except Exception as e:
    print('Aufbau der Verbindung wird gestartet.')
    print('Datenbankverbindung gescheitert')
    print(e)
mycursor = db.cursor()
def createTable(tablename, valueTypeDict, keyP, keyS, refTable, refCol):
    sqlStatement = 'CREATE TABLE' + ' ' + tablename + ' ('
    i = 1
    for column, options in valueTypeDict.items():
        if i < len(valueTypeDict):
            sqlStatement = sqlStatement + column + ' ' + options + ', '
        else:
            sqlStatement = sqlStatement + ' ' + column + ' ' + options
    try:
        sqlStatement = sqlStatement + 'PRIMARY KEY(' + keyP + ')'
        sqlStatement = sqlStatement + 'FOREIGN KEY ('+keyS+') REFERENCES '+refTable+'('+refCol+')'
    except:
        pass
    sqlStatement = sqlStatement + ');'
    print(sqlStatement)
    mycursor.execute(sqlStatement)

def insertData(tablename, columnDataDict):
    sql = 'INSERT INTO' + tablename
    i = 1
    columns = '('
    values = '('
    for column, value in columnDataDict.items():
        if i < len(columnDataDict):
            columns = columns + column + ', ' 
            values = values + value + ', '

def delTask(task):
    sql = 'DELETE FROM tasks WHERE task = "'+task+'"'
    mycursor.execute(sql)
    db.commit()
    print('Datensatz '+task+' angelegt') 

def insertTask(task, prio):
    sql = 'INSERT INTO tasks (idtasks, task, prio) VALUES (NULL, "'+task+'", '+str(prio)+')'
    mycursor.execute(sql)
    db.commit()
    print('Datensatz '+task+' angelegt') 
insertTask("hallo", 1)
#delTask("hallo")


def getTasks():
    sql = "SELECT * FROM tasks"
    mycursor.execute(sql)
    tasks = mycursor.fetchall()
    return tasks
for task in getTasks():
    print(task)
tableName = 'tasks'
tableValues = { 'idtasks'   : 'INT NOT NULL AUTO_INCREMENT',
                'task'      : 'VARCHAR(255) NOT NULL',
                'prio'      : 'TINYINT NULL',
            }


print(tuple(tableValues.values))
    
for key, value in tableValues.items():
    print(key, value)
    print(len(tableValues))
#createTable(tableName, tableValues, 'idtasks', False, False, False)