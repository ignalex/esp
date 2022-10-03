#from time import sleep
from machine import Pin
from pins import INTERNAL_LED, HCSR_TRIGGER, HCSR_SENSOR
from hcsr04 import HCSR04

# hc test
def HCSR(readings=[20,10], limit=300, echo_timeout_us=500*10):
    "[send pulses, min N of positive reply], within limit mm"
    hc = HCSR04(trigger_pin=HCSR_TRIGGER, echo_pin=HCSR_SENSOR, echo_timeout_us=echo_timeout_us)
    READ = []
    for x in range(0,readings[0]):
        try:
            distance = hc.distance_mm()
            READ.append(distance < limit)
        except Exception as e:
            if str(e).find('Out of range') != -1:
                pass
            else:
                print('ERROR getting distance ' + str(e))
    return (len([i for i in READ if i]) >= readings[1], READ)

def hcsr_test(readings=[10,5], limit=100, echo_timeout_us=500*10):
    led = Pin(INTERNAL_LED,Pin.OUT)
    while True:
        read = HCSR(readings, limit,echo_timeout_us)
        led.value(read[0])
        print (read[1])
        #sleep(0.01)
