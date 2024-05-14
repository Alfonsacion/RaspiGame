from time import sleep
from signal import pause
import RPi.GPIO as GPIO
import time

# Desactivar las advertencias de GPIO
GPIO.setwarnings(False)

# Inicializar los pines GPIO para los LEDs y el botón
GPIO.setmode(GPIO.BCM)

led1_pin = 15
led2_pin = 16
led3_pin = 24
led4_pin = 18

button_pin = 22

GPIO.setup(led1_pin, GPIO.OUT)  # Pin del LED 1
GPIO.setup(led2_pin, GPIO.OUT)  # Pin del LED 2
GPIO.setup(led3_pin, GPIO.OUT)  # Pin del LED 3
GPIO.setup(led4_pin, GPIO.OUT)  # Pin del LED 4

# Inicializar el pin GPIO para el botón
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Función para encender los LEDs según el valor ingresado
def encender_led(valor):
    if valor < 45:
        GPIO.output(led1_pin, GPIO.HIGH)
        GPIO.output(led2_pin, GPIO.LOW)
        GPIO.output(led3_pin, GPIO.LOW)
        GPIO.output(led4_pin, GPIO.LOW)
        print("LED 1 ENCENDIDO")

    elif valor < 90:
        GPIO.output(led1_pin, GPIO.LOW)
        GPIO.output(led2_pin, GPIO.HIGH)
        GPIO.output(led3_pin, GPIO.LOW)
        GPIO.output(led4_pin, GPIO.LOW)
        print("LED 2 ENCENDIDO")

    elif valor < 135:
        GPIO.output(led1_pin, GPIO.LOW)
        GPIO.output(led2_pin, GPIO.LOW)
        GPIO.output(led3_pin, GPIO.HIGH)
        GPIO.output(led4_pin, GPIO.LOW)
        print("LED 3 ENCENDIDO")

    else:
        GPIO.output(led1_pin, GPIO.LOW)
        GPIO.output(led2_pin, GPIO.LOW)
        GPIO.output(led3_pin, GPIO.LOW)
        GPIO.output(led4_pin, GPIO.HIGH)
        print("LED 4 ENCENDIDO")

# Bucle principal
try:
    while True:
        # Leer el valor del usuario por teclado
        valor = int(input("Ingrese un valor (0-180): "))
        print("Valor ingresado:", valor)

        # Validar el valor ingresado
        if 0 <= valor <= 180:
            # Esperar hasta que se presione el botón
            print("Esperando a que se presione el botón...")
            GPIO.wait_for_edge(button_pin, GPIO.FALLING)
            time.sleep(0.05)  # Breve pausa para evitar el rebote del botón

            # Encender los LEDs según el valor ingresado
            encender_led(valor)
            print("LEDs encendidos según el valor:", valor)
        else:
            print("El valor debe estar entre 0 y 180.")

finally:
    # Limpiar los pines GPIO
    GPIO.cleanup()
