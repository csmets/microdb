""" Microdb is a mini data handler for python """
import json
import os

path = './mdb/'

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

def fetch_column(db, table, column, q):
    if 'record_id' in q:
        record = fetch_record(db, table, q)
        return list(map(
            lambda c: c[column],
            record))
    else:
        print('record_id key is missing from query')

def fetch_record(db, table, q):
    if 'record_id' in q:
        return list(filter(
            lambda r: r[q['record_id']['key']] == q['record_id']['value'],
            db[table]))
    else:
        print('record_id key is missing from query')

def update_table(db, table, record):
    db[table].update(record)
    return db

def insert_to_column(db, table, column, q):
    """ Insert into a column """
    if 'record_id' in q:
        def update_column(record):
            if record[q['record_id']['key']] == q['record_id']['value']:
                record[column] = q['value']
            return record

        db[table] = list(map(update_column, db[table]))

        return db
    else:
        print('record_id key is missing from query')

def insert_to_table(db, table, q):
    """ insert record into table or update an existing record if given query """
    if 'record_id' in q:
        def update_record(record):
            if record[q['record_id']['key']] == q['record_id']['value']:
                for key in record:
                    if key in q['value']:
                        record[key] = q['value'][key]
            return record

        db[table] = list(map(update_record, db[table]))

        return db
    else:
        db[table].append(q)

    return db

def remove_table_record(db, table, q):
    if 'record_id' in q:
        removed = list(filter(
            lambda r: r[q['record_id']['key']] != q['record_id']['value'],
            db[table]))
        db[table] = removed
        return db
    else:
        print('record_id key is missing from query')

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

    # Table column (dict, string, string, func, args*)
    if (isinstance(args[0], dict) and isinstance(args[1], str) and
            isinstance(args[2], str) and callable(args[3])):

        query_args = args[4:]
        def column_loop(i, db):
            if i > 0:
                i = i - 1
                return column_loop(
                    i,
                    args[3](args[0], args[1], args[2], query_args[i])
                )

            return db

        return column_loop(len(query_args), args[0])

    return False
