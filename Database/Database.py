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


def create_transaction_table():
    try:
        connection, cursor = open_connection()
        query = """CREATE TABLE IF NOT EXISTS Transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_number INTEGER,
                    customer_id int,
                    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id))"""

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


def create_customer(customer):
    query = "INSERT INTO Customers VALUES (? ,?, ?)"
    parameters = (customer.customer_id, customer.customer_name, customer.customer_last_name)
    querry_database(query, parameters)


def get_customer():
    query = "SELECT * FROM Customers"
    querry_database(query)


def create_transaction(transaction, customer_id):
    query = "INSERT INTO Transactions VALUES (? ,?, ?)"
    parameters = (transaction.transaction_id, transaction.transaction_number, customer_id)
    querry_database(query, parameters)


def get_transaction():
    query = "SELECT * FROM Transactions"
    querry_database(query)


# def update_customer(customer_id, transaction_id):
#     query = """UPDATE Customers SET transaction_id = ? WHERE customer_id = ?"""
#     parameters = (transaction_id, customer_id)
#     querry_database(query, parameters)


def insert_record(customer, transaction):
    create_customer(customer)

    connection, cursor = open_connection()

    customer_id_for_transaction = cursor.execute("SELECT customer_id FROM Customers WHERE customer_name = (?)", (customer.customer_name,)).fetchone()


    connection.close()

    customer.customer_id = customer_id_for_transaction[0]

    create_transaction(transaction, customer.customer_id)

    # connection, cursor = open_connection()
    #
    # # transaction_id_for_customer = cursor.execute("SELECT transaction_id FROM Transactions ORDER BY transaction_id DESC").fetchone()
    #
    # close_connection(connection, cursor)
    #
    # transaction.transaction_id = transaction_id_for_customer[0]
    #
    # update_customer(customer.customer_id, transaction.transaction_id)


customer1 = Customer(None, "Jonas","Jonaitis")
transaction1 = Transaction(None, 548795, None)

create_customers_table()
create_transaction_table()
# create_customer(customer1.customer_id, customer1.customer_name, customer1.customer_last_name)
# create_transaction(transaction1)
insert_record(customer1, transaction1)
get_customer()
get_transaction()
