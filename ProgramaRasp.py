# Bibliotecas
import board
import adafruit_bmp280
import RPi.GPIO as GPIO
import time
from time import sleep
import busio
import adafruit_adxl34x
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import paho.mqtt.client as mqtt

# Setup lecturas
# BMP setup
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(board.I2C(), address=0x76)
bmp280.sea_level_pressure = 1013.25
# Acelerometro
i2c = busio.I2C(board.SCL, board.SDA)
accel = adafruit_adxl34x.ADXL345(i2c, 0x53)
# ADS
I2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(I2c)
# Define el canal de lectura del ADS
channel = AnalogIn(ads, ADS.P0)
# bmp
temp = bmp280.temperature
press = bmp280.pressure
alt = bmp280.altitude
# Acelerometro
acceleration = ("%f_%f_%f" % accel.acceleration)
# Voltaje analogico
Valor_Analogico = channel.value
Voltaje = channel.voltage
# Setup de lectura distancia
TRIG = 23
ECHO = 24
print("medicion en progreso")
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("esperando datos")
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)
while GPIO.input(ECHO) == 0:
    pulse_start = time.time()

while GPIO.input(ECHO) == 1:
    pulse_end = time.time()
# Distancia
pulso_dura = pulse_end - pulse_start
dist = pulso_dura * 17150
dist = round(dist, 2)


# SETUP DE HIVE (Mandar mensaje)

def on_publish(client, userdata, mid, reason_code, properties):
    try:
        userdata.remove(mid)
    except KeyError:
        print("Error")


unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect("broker.hivemq.com", 1883)

mqttc.loop_start()

# Setup de Motores
GPIO.setmode(GPIO.BCM)

Motor11 = 16
Motor12 = 21
Motor13 = 20
Motor21 = 13
Motor22 = 19
Motor23 = 26

GPIO.setup(Motor11, GPIO.OUT)
GPIO.setup(Motor12, GPIO.OUT)
GPIO.setup(Motor13, GPIO.OUT)

GPIO.setup(Motor21, GPIO.OUT)
GPIO.setup(Motor22, GPIO.OUT)
GPIO.setup(Motor23, GPIO.OUT)


# movimiento del carrito
def adelante():
    # Empieza a avanzar hacia adelante
    GPIO.output(Motor11, GPIO.HIGH)
    GPIO.output(Motor12, GPIO.HIGH)
    GPIO.output(Motor13, GPIO.LOW)

    GPIO.output(Motor21, GPIO.HIGH)
    GPIO.output(Motor22, GPIO.LOW)
    GPIO.output(Motor23, GPIO.HIGH)


def atras():
    # Empieza a avanzar hacia atras
    GPIO.output(Motor11, GPIO.LOW)
    GPIO.output(Motor12, GPIO.HIGH)
    GPIO.output(Motor13, GPIO.HIGH)
    GPIO.output(Motor21, GPIO.HIGH)
    GPIO.output(Motor22, GPIO.HIGH)
    GPIO.output(Motor23, GPIO.LOW)


def izquierda():
    # Empieza a avanzar hacia la izquierda
    GPIO.output(Motor11, GPIO.HIGH)
    GPIO.output(Motor12, GPIO.HIGH)
    GPIO.output(Motor13, GPIO.LOW)
    GPIO.output(Motor21, GPIO.HIGH)
    GPIO.output(Motor22, GPIO.HIGH)
    GPIO.output(Motor23, GPIO.LOW)


def derecha():
    # Empieza a avanzar hacia la derecha
    GPIO.output(Motor11, GPIO.LOW)
    GPIO.output(Motor12, GPIO.HIGH)
    GPIO.output(Motor13, GPIO.HIGH)
    GPIO.output(Motor21, GPIO.HIGH)
    GPIO.output(Motor22, GPIO.LOW)
    GPIO.output(Motor23, GPIO.HIGH)


# Enviado de mensaje al hive
def mandar_mensaje():
    # Lectores
    # Publicar mensajes
    msg_info1 = mqttc.publish("vsciot/adc", f"adc_{Valor_Analogico}_{Voltaje}", qos=2)
    unacked_publish.add(msg_info1.mid)
    msg_info2 = mqttc.publish("vsciot/bmp", f"bmp_{temp}{press}{alt}", qos=2)
    unacked_publish.add(msg_info2.mid)
    msg_info5 = mqttc.publish("vsciot/acelerometro", f"acelerometro_{acceleration}", qos=2)
    unacked_publish.add(msg_info5.mid)
    msg_info9 = mqttc.publish("vsciot/ultrasonico", f"ultrasonico_{dist}", qos=2)
    unacked_publish.add(msg_info9.mid)

    # Esperando a publicar el mnesaje
    while len(unacked_publish):
        time.sleep(0.1)

    msg_info1.wait_for_publish()
    msg_info2.wait_for_publish()
    msg_info5.wait_for_publish()
    msg_info9.wait_for_publish()


#############Inicio del codigo#############
segundos = 0
carro = True
print("Adelante")
adelante()
while carro:
    # Contador
    segundos += 1
    # Lectores
    mandar_mensaje()
    # Para despues de 5 segundos
    if segundos == 30:
        carro = False
        GPIO.output(Motor11, GPIO.LOW)
        GPIO.output(Motor12, GPIO.HIGH)
        GPIO.output(Motor13, GPIO.LOW)
        GPIO.output(Motor21, GPIO.LOW)
        GPIO.output(Motor22, GPIO.HIGH)
        GPIO.output(Motor23, GPIO.LOW)

segundos = 0
print("Atras")
atras()
carro = True
while carro:
    # Contador
    segundos += 1
    # Lectores
    mandar_mensaje()
    # Para despues de 5 segundos
    if segundos == 2:
        carro = False
        GPIO.output(Motor11, GPIO.LOW)
        GPIO.output(Motor12, GPIO.HIGH)
        GPIO.output(Motor13, GPIO.LOW)
        GPIO.output(Motor21, GPIO.LOW)
        GPIO.output(Motor22, GPIO.HIGH)
        GPIO.output(Motor23, GPIO.LOW)

segundos = 0
print("Izquierda")
izquierda()
carro = True
while carro:
    # Contador
    segundos += 1
    # Lectores
    mandar_mensaje()
    # Para despues de 5 segundos
    if segundos == 2:
        carro = False
        GPIO.output(Motor11, GPIO.LOW)
        GPIO.output(Motor12, GPIO.HIGH)
        GPIO.output(Motor13, GPIO.LOW)
        GPIO.output(Motor21, GPIO.LOW)
        GPIO.output(Motor22, GPIO.HIGH)
        GPIO.output(Motor23, GPIO.LOW)

segundos = 0
print("Derecha")
derecha()
carro = True
while carro:
    # Contador
    segundos += 1
    time.sleep(1)
    # Lectores
    mandar_mensaje()
    # Para despues de 5 segundos
    if segundos == 2:
        carro = False
        GPIO.output(Motor11, GPIO.LOW)
        GPIO.output(Motor12, GPIO.HIGH)
        GPIO.output(Motor13, GPIO.LOW)
        GPIO.output(Motor21, GPIO.LOW)
        GPIO.output(Motor22, GPIO.HIGH)
        GPIO.output(Motor23, GPIO.LOW)