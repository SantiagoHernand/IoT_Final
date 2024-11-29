import time

from database_manager import DatabaseManager
import paho.mqtt.client as mqtt

db_manager = DatabaseManager('10.48.241.219', 'raspberry_database', 'vsciot', 'tucola2')


def on_message(client, userdata, msg):
    try:
        msg = msg.payload.decode()

        msg_split = msg.split("_")
        sensor = msg_split[0].lower()

        if sensor == "adc":
            luz_valor = msg_split[1]
            voltaje = msg_split[2]
            db_manager.insert_adc(luz_valor, voltaje)
            print(f"ADC: Valor={luz_valor}, Voltaje={voltaje}")

        elif sensor == "acelerometro":
            valor_x = msg_split[1]
            valor_y = msg_split[2]
            valor_z = msg_split[3]
            db_manager.insert_acelerometro(valor_x, valor_y, valor_z)
            print(f"Acelerómetro: X={valor_x}, Y={valor_y}, Z={valor_z}")

        elif sensor == "bmp":
            temperatura = msg_split[1]
            presion = msg_split[2]
            altitud = msg_split[3]
            db_manager.insert_presion(temperatura, presion, altitud)
            print(f"BMP: Temp={temperatura}, Presión={presion}, Altitud={altitud}")

        elif sensor == "ultrasonico":
            distancia = msg_split[1]
            db_manager.insert_ultrasonico(distancia)
            print(f"Ultrasonico: Distancia={distancia} cm")

    except Exception as e:
        print(f"Error: {e}")



unacked_publish = set()
mqtt_client = mqtt.Client()

mqtt_client.on_message = on_message

topics = ["vsciot/adc", "vsciot/bmp", "vsciot/ultrasonico", "vsciot/acelerometro"]

try:
    mqtt_client.connect("broker.hivemq.com", 1883)
    print("Se conecto al broker")

    # Suscripción dinámica
    for topic in topics:
        mqtt_client.subscribe(topic)

except Exception as e:
    exit()

mqtt_client.loop_start()
try:
    while True:
        time.sleep(1)
except:
    print(f"Error")
finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
