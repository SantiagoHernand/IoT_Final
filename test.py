from database_manager import DatabaseManager
db_manager = DatabaseManager('10.48.241.219', 'raspberry_database', 'vsciot', 'tucola2')

valor = 0;
voltaje = 10;
db_manager.insert_adc(valor)

x = 20
y = 30
z=40
db_manager.insert_acelerometro(x, y, z)

db_manager.insert_presion(x, y, z)

dist = 40

db_manager.insert_ultrasonico(dist)