import json
import os

path = './mdb/'

'''
Micro DB requirements

1. load up a database file
2. Create a table
3. Insert a record
4. Insert into a column
5. Update a record
6. Update a column
7. Find a record using a column key and value and reference
8. Delete a column
9. Delete a record
10. Check if table exists
11. Check if column exists
12. Fetch a table
13. Fetch a column
14. Write database
15. Compose

'''

# Write contents into a file
def write(filename, content):
    wpath = os.path.dirname(filename)
    if not os.path.exists(wpath):
        os.makedirs(wpath)
    f = open(filename, 'w')
    f.write(content)
    f.close()

# Load up the database
def opendb(name):
    dbfile = path + name + '.json'
    if not os.path.isfile(dbfile):
        write(dbfile, '{}')
    f = open(dbfile)
    string = f.read()
    return json.loads(string)

# Write out the database to a file
def closedb(db, name):
    dbfile = path + name + '.json'
    jsonOut = json.dumps(db, indent = 4, sort_keys = True)
    write(dbfile, jsonOut)

# Check if a table exists
def tableExist(db, table):
    if table in db:
        return True
    else:
        return False

# Create a new table
def createTable(db, name):
    if not tableExist(db, name):
        db[name] = []
    else:
        raise ValueError('Table already exists!')
    return db

# Check if a column exists
def columnExist(table, column):
    if column in table:
        return True
    else:
        return False

# Create a column within a table
def createColumn(db, table, column):
    db[table][column] = {}
    return db

# Get table contents
def fetchTable(db, table):
    if tableExists(db, table):
        return db[table]
    else:
        raise ValueError('Table doesn\'t exist!')

# Get column contents from table
def fetchColumnFrom(db, table):
    def column(name):
        return db[table][name]
    return column

# Update the table with an updated record
def updateTable (db, table):
    def update(content):
        db[table].update(content)
        return db
    return update

# Add a new entry into a column
def insertToColumn(db, table):
    def write(column, content):
        db[table][column] = content
        return db
    return write

# Insert a new record into a table
def insertToTable(db, table):
    def insert(content):
        db[table].append(content)
        return db
    return insert

# Delete table record
def removeTableRecord(db, table):
    def record(row):
       del db[table][row]
       return db
    return record

# TODO Create a query function that will append an action to the database
def query(db, *functions):
    return

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)),
            functions, lambda x: x)
