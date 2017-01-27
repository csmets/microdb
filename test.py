import micro_db

mydb = micro_db.opendb('MyDB')
addTable = micro_db.createTable(mydb, 'users')
user1 = {
    "name": "Bob",
    "password": "12345"
}

user2 = {
    "name": "Macy",
    "password": "1234567"
}

addRecord = micro_db.insertToTable(addTable, 'users')
addedRecord = addRecord(user1)

addRecord2 = micro_db.insertToTable(addedRecord, 'users')
addedRecord2 = addRecord2(user2)

micro_db.closedb(addedRecord2, 'MyDB')
