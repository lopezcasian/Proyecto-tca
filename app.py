import RPi.GPIO as GPIO        
from gpiozero import LightSensor, MotionSensor
from flask import Flask, render_template, request, json
app = Flask(__name__)

GPIO.setmode(GPIO.BCM) #Modo de pins

pins = {
   23 : {'nombre' : 'Foco1', 'estado' : GPIO.LOW},
   24 : {'nombre' : 'Foco2', 'estado' : GPIO.LOW}
   } #Diccionario pins

for pin in pins: # COnfigurar como salida y apagar pins
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def index():
   return render_template('index.html') # Ventana principal y unica

@app.route("/manual/<gpioU>/<accion>", methods=['POST'])
def action(gpioU, accion):
   
   gpioU = int(gpioU) # Parametro de pin debe ser entero
   
   if accion == "on": # Comparando el parametro accion
      GPIO.output(gpioU, GPIO.HIGH)
      mensaje = "Encendido."
   if accion == "off":
      GPIO.output(gpioU, GPIO.LOW)
      mensaje = "Apagado"
      
   for pin in pins: #Cambiando el estado del diccionario pins
      pins[pin]['estado'] = GPIO.input(pin)

   return json.dumps({'status':'OK', 'estado': mensaje}) # Se envia respuesta a archivo script.js
	
@app.route('/automatico', methods=['POST'])
def automatico():
   ldr = LightSensor(17) # Sensor de luz en pin 17 del raspberry
   pir = MotionSensor(4) # Sensor de movimiento en el pin 4

   if pir.motion_detected: # Si hay movimiento
      movimiento = "Si"
      if (int(ldr.value * 100) >= 0) and (int(ldr.value * 100) <= 60): # Poca luz, se encienden los dos focos
            GPIO.output(23, GPIO.HIGH)
            GPIO.output(24, GPIO.HIGH)
            print(int(ldr.value * 100))
            foco1 = "Encendido"
            foco2 = "Encendido"
            luz = "Poca o nada"

      elif (int(ldr.value * 100) > 60) and (int(ldr.value * 100) <= 70): # Media luz, se enciende solo un foco
            GPIO.output(23, GPIO.HIGH)
            GPIO.output(24, GPIO.LOW)
            print(int(ldr.value * 100))
            foco1 = "Encendido"
            foco2 = "Apagado"
            luz = "Media"
      elif (int(ldr.value * 100) > 70): # Mucha luz, se apagan los dos focos
            GPIO.output(23, GPIO.LOW)
            GPIO.output(24, GPIO.LOW)
            print(int(ldr.value * 100))
            foco1 = "Apagado"
            foco2 = "Apagado"
            luz = "Bastante"
   else: #si no hay movimiento se apagan los dos focos
      movimiento = "No"
      GPIO.output(23, GPIO.LOW)
      GPIO.output(24, GPIO.LOW)
      foco1 = "Apagado"
      foco2 = "Apagado"
      if (int(ldr.value * 100) >= 0) and (int(ldr.value * 100) <= 60):
            print(int(ldr.value * 100))
            luz = "Poca o nada"

      elif (int(ldr.value * 100) > 60) and (int(ldr.value * 100) <= 70):
            print(int(ldr.value * 100))
            luz = "Media"
            
      elif (int(ldr.value * 100) > 70):
            print(int(ldr.value * 100))
            luz = "Bastante"


   return json.dumps({'status':'OK-automatico','luz':luz, '1':foco1, '2':foco2, 'mov':movimiento}) # Se envia respuesta a archivo script.js

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
