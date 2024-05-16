from gpiozero import Buzzer, Button
from time import sleep
from signal import pause

# importamos la libreria GPIO
import RPi.GPIO as GPIO
# desactivamos mensajes de error
GPIO.setwarnings(False)
# indicamos el uso de  la identificacion BCM para los GPIO
GPIO.setmode(GPIO.BCM)
# indicamos que el GPIO18 es de salida de corriente
GPIO.setup(18,GPIO.OUT)
# damos corriente al pin
GPIO.output(18, True)

buzzer = Buzzer(18)

button = Button(22)


def disparar():
  button.wait_for_release()
  buzzer.on()
  sleep(0.1)
  buzzer.off()


while True:
  disparar()
  
  
  
  
  

  
  
  
  

