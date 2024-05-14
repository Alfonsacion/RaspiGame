from __future__ import print_function
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 50)
pwm.start(2.5)

# Configurar pines para botones
boton_izquierda = 5
boton_derecha = 16
GPIO.setup(boton_izquierda, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boton_derecha, GPIO.IN, pull_up_down=GPIO.PUD_UP)

angulo = 0  # Inicializar el ángulo del servo

# Función para aumentar el ángulo
def aumentar(channel):
    global angulo
    angulo += 5
    if angulo > 180:
        angulo = 180
    print("Angulo actual:", angulo)

# Función para disminuir el ángulo
def disminuir(channel):
    global angulo
    angulo -= 5
    if angulo < 0:
        angulo = 0
    print("Angulo actual:", angulo)

# Configurar interrupciones para los botones con bouncetime reducido
GPIO.add_event_detect(boton_izquierda, GPIO.FALLING, callback=aumentar, bouncetime=100)
GPIO.add_event_detect(boton_derecha, GPIO.FALLING, callback=disminuir, bouncetime=100)

try:
    while True:
        duty = angulo / 18 + 2.5
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.05)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
