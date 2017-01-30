# Microdb
Small lightweight JSON handler created for Python. It doesn't prove to boast that it fully packed with features and data manipulation and handling, rather it's focus on the minimal tasks required for fetching/insert/updating data.

## Example usage
```python
import microdb

mydb = microdb.opendb('MyDatabase')
customers_table = microdb.create_table('customers')

user1 = {
    'name': 'Jack',
    'job': 'Pirate',
    'paid': True
}

user2 = {
    'name': 'Lucy',
    'job': 'Ninja',
    'paid': True
}

# Query(<dict> Database, <string> table, <func> action, <any> ..arg)
customers = microdb.query(
    customer_table,
    'customers',
    microdb.insert_to_table,
    user1,
    user2
)

microdb.closedb(customers, 'MyDatabase')
```
