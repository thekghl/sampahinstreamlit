import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Change if needed
        password="",         # Fill with your MySQL password
        database="pelaporan_sampah"
    )