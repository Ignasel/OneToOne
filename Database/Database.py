transaction_table="Transaction"
customer_table="Customer"

import sqlite3
from Customers_Trans.Customers import Customer
from Customers_Trans.Transactions import Transaction


def open_connection():
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def create_transaction_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS Transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_number INTEGER)"""

        cursor.execute(query)
        connection.commit()

    except sqlite3.DatabaseError as error:
        print(error)

    finally:
        close_connection(connection, cursor)


def create_customers_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS Customers (
                    customer_id integer PRIMARY KEY AUTOINCREMENT,
                    customer_name text,
                    customer_last_name text)
                """

        cursor.execute(query)
        connection.commit()

    except sqlite3.DatabaseError as error:
        print(error)

    finally:
        close_connection(connection, cursor)


def querry_database(query, parameters=None):
    try:
        connection, cursor = open_connection()
        if parameters:
            cursor.execute(query, parameters)
            connection.commit()
        else:
            for row in cursor.execute(query):
                print(row)
    except sqlite3.DataError as error:
        print(error)
    finally:
        connection.close()


def create_customer(customer_id, customer_name, customer_last_name):
    query = "INSERT INTO Customers VALUES (? ,?, ?)"
    parameters = (customer_id, customer_name, customer_last_name)
    print(parameters)
    querry_database(query, parameters)


def get_customer():
    query = "SELECT * FROM Customers"
    querry_database(query)


def create_transaction(transaction):
    query = "INSERT INTO Transactions VALUES (? ,?)"
    parameters = (transaction.transaction_id, transaction.transaction_number)
    querry_database(query, parameters)


def get_transaction():
    query = "SELECT * FROM Transactions"
    querry_database(query)


customer1 = Customer(None, "Jonas","Jonaitis")
transaction1 = Transaction(None, 548795)


create_transaction_table()
create_customers_table()
create_customer(customer1.customer_id, customer1.customer_name, customer1.customer_last_name)
create_transaction(transaction1)
get_customer()
get_transaction()
