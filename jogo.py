from __future__ import print_function
import RPi.GPIO as GPIO
from gpiozero import Buzzer, Button
import time, sys
import random

# Configuración inicial
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Configurar pines para el servo
pin_servo = 12
GPIO.setup(pin_servo, GPIO.OUT)
pwm = GPIO.PWM(pin_servo, 50)
pwm.start(2.5)

# Configurar pines para los botones del servo
pin_boton_izquierdo = 5
pin_boton_derecho = 16
GPIO.setup(pin_boton_izquierdo, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_boton_derecho, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configurar el buzzer
pin_buzzer = 18
buzzer = Buzzer(pin_buzzer)
pin_boton_buzzer = 22

# Configurar pines para los LEDs
pines_led = [15, 26, 24]
for pin in pines_led:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Inicializar el pin GPIO para el botón del buzzer
boton_buzzer = Button(pin_boton_buzzer)

# Inicializar el ángulo del servo
angulo = 0

# Inicializar contadores
disparos = 0
aciertos = 0
led_actual = None

# Establecer límite de tiempo (30 segundos)
limite_tiempo = 30
tiempo_inicio = time.time()
tiempo_terminado = False

# Funciones para cambiar el ángulo del servo
def aumentar_angulo(channel):
    global angulo
    angulo += 5
    if angulo > 180:
        angulo = 180
    print("Ángulo actual:", angulo)

def disminuir_angulo(channel):
    global angulo
    angulo -= 5
    if angulo < 0:
        angulo = 0
    print("Ángulo actual:", angulo)

# Configurar interrupciones para los botones del servo
GPIO.add_event_detect(pin_boton_izquierdo, GPIO.FALLING, callback=aumentar_angulo, bouncetime=100)
GPIO.add_event_detect(pin_boton_derecho, GPIO.FALLING, callback=disminuir_angulo, bouncetime=100)

# Función para encender un LED aleatorio
def encender_led_aleatorio():
    global led_actual
    if led_actual is not None:
        GPIO.output(led_actual, GPIO.LOW)
    led_actual = random.choice(pines_led)
    GPIO.output(led_actual, GPIO.HIGH)
    print(f"LED {pines_led.index(led_actual) + 1} ENCENDIDO")

# Función para verificar si el servo está dentro del rango del LED encendido
def esta_en_rango_acierto(angulo):
    if led_actual == pines_led[0] and 20 <= angulo < 40:
        return True
    elif led_actual == pines_led[1] and 80 <= angulo < 100:
        return True
    elif led_actual == pines_led[2] and 140 <= angulo < 160:
        return True
    return False

# Función para activar el buzzer y manejar los aciertos
def activar_buzzer_y_leds():
    global disparos, aciertos, tiempo_terminado
    if tiempo_terminado:
        return
    buzzer.on()
    time.sleep(0.1)
    buzzer.off()
    disparos += 1
    if esta_en_rango_acierto(angulo):
        aciertos += 1
    precision = (aciertos / disparos) * 100 if disparos > 0 else 0
    precision_redondeada = round(precision, 0)
    print(f"Disparos: {disparos}, Aciertos: {aciertos}, Tasa de aciertos: {precision:.2f}%")
    encender_led_aleatorio()

# Asignar el botón del buzzer a la función que también enciende los LEDs
boton_buzzer.when_pressed = activar_buzzer_y_leds

# Inicializar encendiendo un LED aleatorio
encender_led_aleatorio()

try:
    while True:
        # Verificar si se ha alcanzado el límite de tiempo
        tiempo_transcurrido = time.time() - tiempo_inicio
        if tiempo_transcurrido > limite_tiempo and not tiempo_terminado:
            # Encender todos los LEDs
            for pin in pines_led:
                GPIO.output(pin, GPIO.HIGH)
            # Activar el buzzer tres veces
            for _ in range(3):
                buzzer.on()
                time.sleep(0.1)
                buzzer.off()
                time.sleep(0.1)
            precision = (aciertos / disparos) * 100 if disparos > 0 else 0
            precision_redondeada = round(precision, 0)
            print(f"¡Tiempo terminado! Disparos: {disparos}, Aciertos: {aciertos}, Tasa de aciertos: {precision:.2f}%")
            tiempo_terminado = True

        if not tiempo_terminado:
            # Cambiar la posición del servo
            ciclo_trabajo = angulo / 18 + 2.5
            pwm.ChangeDutyCycle(ciclo_trabajo)
            time.sleep(0.05)
        else:
            time.sleep(0.5)  # Reducir la velocidad del bucle cuando se termina el tiempo

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
