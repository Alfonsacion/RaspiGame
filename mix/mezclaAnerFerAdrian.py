from __future__ import print_function
import RPi.GPIO as GPIO
import time
from gpiozero import Buzzer, Button

# Configuracion inicial
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Configurar pines para el servo
servo_pin = 12
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(2.5)

# Configurar pines para los botones del servo
button_left_pin = 5
button_right_pin = 16  
GPIO.setup(button_left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configurar el buzzer
buzzer_pin = 18
buzzer = Buzzer(buzzer_pin)
button_buzzer_pin = 22

# Configurar pines para los LEDs
led1_pin = 15
led2_pin = 24  
led3_pin = 26
led4_pin = 1 

GPIO.setup(led1_pin, GPIO.OUT)  # Pin del LED 1
GPIO.setup(led2_pin, GPIO.OUT)  # Pin del LED 2
GPIO.setup(led3_pin, GPIO.OUT)  # Pin del LED 3
GPIO.setup(led4_pin, GPIO.OUT)  # Pin del LED 4

# Inicializar el pin GPIO para el boton del buzzer
button_buzzer = Button(button_buzzer_pin)

# Inicializar el angulo del servo
angle = 0

# Funciones para cambiar el angulo del servo
def increase_angle(channel):
    global angle
    angle += 5
    if angle > 180:
        angle = 180
    print("Angulo actual:", angle)

def decrease_angle(channel):
    global angle
    angle -= 5
    if angle < 0:
        angle = 0
    print("Angulo actual:", angle)

# Configurar interrupciones para los botones del servo
GPIO.add_event_detect(button_left_pin, GPIO.FALLING, callback=increase_angle, bouncetime=100)
GPIO.add_event_detect(button_right_pin, GPIO.FALLING, callback=decrease_angle, bouncetime=100)

# Funcion para encender los LEDs segun el angulo
def encender_led(angle):
    if angle < 45:
        GPIO.output(led1_pin, GPIO.HIGH)
        GPIO.output(led2_pin, GPIO.LOW)
        GPIO.output(led3_pin, GPIO.LOW)
        GPIO.output(led4_pin, GPIO.LOW)
        print("LED 1 ENCENDIDO")
    elif angle < 90:
        GPIO.output(led1_pin, GPIO.LOW)
        GPIO.output(led2_pin, GPIO.HIGH)
        GPIO.output(led3_pin, GPIO.LOW)
        GPIO.output(led4_pin, GPIO.LOW)
        print("LED 2 ENCENDIDO")
    elif angle < 135:
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

# Funcion para activar el buzzer y los LEDs
def activate_buzzer_and_leds():
    buzzer.on()
    time.sleep(0.1)
    buzzer.off()
    encender_led(angle)

# Asignar el boton del buzzer a la funcion que tambien enciende los LEDs
button_buzzer.when_pressed = activate_buzzer_and_leds

try:
    while True:
        # Cambiar la posicion del servo
        duty = angle / 18 + 2.5
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.05)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
