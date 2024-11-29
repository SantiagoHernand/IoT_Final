import mysql.connector
from mysql.connector import Error
from datetime import datetime


fecha = datetime.now()

class DatabaseManager:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='10.48.241.219',
                database='raspberry_database',
                user='vsciot',
                password='tucola2'
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
        except Error as e:
            print(e)

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def insert_producto(self, name, description, price, weight):
        query = """INSERT INTO producto (nombre, descripcion, precio, peso) VALUES (%s,%s,%s,%s)"""
        values = (name, description, price, weight)
        self.cursor.execute(query, values)
        self.connection.commit()

    def list_sensor(self,sensor):
        query = f"SELECT * FROM {sensor}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            print(row[1])

    def insert_adc(self, luz_valor, voltaje):
        query = """INSERT INTO adc (fecha, luz_valor, voltaje) VALUES (%s,%s, %s)"""
        values = (fecha,luz_valor,voltaje)
        self.cursor.execute(query, values,)
        self.connection.commit()

    def insert_acelerometro(self, valor_x,valor_y,valor_z):
        query = """INSERT INTO acelerometro ( fecha,valor_x,valor_y,valor_z) VALUES (%s,%s,%s,%s)"""
        values = ( fecha,valor_x,valor_y,valor_z)
        self.cursor.execute(query, values,)
        self.connection.commit()

    def insert_presion(self, temp,presion,altitud):
        query = """INSERT INTO bmp (fecha,temp,presion,altitud) VALUES (%s,%s,%s,%s)"""
        values = (fecha,temp,presion,altitud)
        self.cursor.execute(query, values)
        self.connection.commit()

    def insert_ultrasonico(self, distancia_valor):
        query = """INSERT INTO ultrasonico ( fecha,distancia_valor) VALUES (%s,%s)"""
        values = ( fecha,distancia_valor,)
        self.cursor.execute(query, values)
        self.connection.commit()