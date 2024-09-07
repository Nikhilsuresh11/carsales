from dj_database_url import DBConfig
import mysql.connector.plugins
import pymysql
import pymysql

connection = pymysql.connect(host='localhost', user='root', password='1234', database='cars')



print("ALL DONE!")