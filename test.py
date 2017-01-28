""" File for testing microdb """

import microdb

mydb = microdb.opendb('MyDB')
add_table = microdb.create_table(mydb, 'users')
user1 = {
    "fname": "Bob",
    "lname": "Schmitty",
    "password": "12345"
}

user2 = {
    "fname": "Macy",
    "lname": "Lu",
    "password": "1234567"
}

user3 = {
    "fname": "Lisa",
    "lname": "Mona",
    "password": "1234567"
}

added = microdb.query(
    add_table,
    'users',
    microdb.insert_to_table,
    user1,
    user2,
    user3
)

update_column = microdb.query(
    added,
    'users',
    'password',
    microdb.insert_to_column,
    {'record_id': {'key': 'fname', 'value': 'Macy'}, 'value': 'poo'}
)

update_record = microdb.query(
    update_column,
    'users',
    microdb.insert_to_table,
    {'record_id': {'key': 'fname', 'value': 'Lisa'}, 'value': {'lname': 'Rabbit', 'fname': 'Peter'}}
)

find_macy = microdb.fetch_record(
    update_record,
    'users',
    {'record_id': {'key': 'fname', 'value': 'Macy'}}
)

delete_macy = microdb.remove_table_record(
    update_record,
    'users',
    {'record_id': {'key': 'lname', 'value': 'Lu'}}
)

dump_table = microdb.fetch_column(
    delete_macy,
    'users',
    'fname',
    {'record_id': {'key': 'lname', 'value': 'Rabbit'}}
)

microdb.closedb(added, 'MyDB')
