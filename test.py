""" File for testing microdb """

import microdb

mydb = microdb.opendb('MyDB')
add_table = microdb.create_table(mydb, 'users')
user1 = {
    "name": "Bob",
    "password": "12345"
}

user2 = {
    "name": "Macy",
    "password": "1234567"
}

user3 = {
    "name": "Lisa",
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
    dict({'key': 'name', 'value': 'Macy'}),
    microdb.insert_to_column,
    '5555'
)

print(update_column)

# microdb.closedb(added, 'MyDB')
