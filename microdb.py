""" Mircodb is a mini data handler for python """
import json
import os

path = './mdb/'

'''
Micro DB requirements

1. load up a database file -DONE
2. Create a table -DONE
3. Insert a record -DONE
5. Update a record
6. Update a column -DONE
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
    json_out = json.dumps(db, indent=4, sort_keys=True)
    write(dbfile, json_out)

def table_exist(db, table):
    return bool(table in db)

def create_table(db, name):
    if not table_exist(db, name):
        db[name] = []
    else:
        raise ValueError('Table already exists!')
    return db

def column_exist(table, column):
    return bool(column in table)

def create_column(db, table, column):
    db[table][column] = {}
    return db

def fetch_table(db, table):
    if table_exist(db, table):
        return db[table]
    else:
        raise ValueError('Table doesn\'t exist!')

def fetch_column(db, table, column):
    return db[table][column]

def update_table(db, table, record):
    db[table].update(record)
    return db

def insert_to_column(db, table, column, record_id, content):
    """ Insert into a column """
    def map_func(record):
        if record[record_id['key']] == record_id['value']:
            record[column] = content
            return record
        else:
            return record

    db[table] = list(map(map_func, db[table]))

    return db

def insert_to_table(db, table, content):
    db[table].append(content)
    return db

def remove_table_record(db, table, row):
    del db[table][row]
    return db

def query(*args):
    """ Execute a database query """

    # Table query actions (dict, string, func, args*)
    if (isinstance(args[0], dict) and isinstance(args[1], str) and
            callable(args[2])):
        query_args = args[3:]
        def table_loop(i, db):
            if i > 0:
                i = i - 1
                return table_loop(i, args[2](args[0], args[1], query_args[i]))

            return db

        return table_loop(len(query_args), args[0])

    # Table column (dict, string, dict, string, func, args*)
    if (isinstance(args[0], dict) and isinstance(args[1], str) and
            isinstance(args[2], str) and isinstance(args[3], dict) and
            callable(args[4])):

        query_args = args[5:]
        def column_loop(i, db):
            if i > 0:
                i = i - 1
                return column_loop(
                    i,
                    args[4](args[0], args[1], args[2], args[3], query_args[i])
                )

            return db

        return column_loop(len(query_args), args[0])

    return False
