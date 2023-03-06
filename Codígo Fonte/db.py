import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "DB_SQL", "DataBase/Return_System.db")


def execute_query(query, args=(), fetchall=False):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        return cursor.fetchall() if fetchall else cursor.fetchone()


def dql(query):  # select, popular
    return execute_query(query, fetchall=True)


def dml(query):  # inserir, Delete, Update
    execute_query(query)


def lgn(query):  # login
    return execute_query(query)
