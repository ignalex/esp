# ESP module control with python

* **IMPORTANT**: no security other http built. used to be sitting in the internal wifi.

## setup
- https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html

## FILES

### boot
1st run on start - generic

### main
2nd run on start - specific
* assign IP, SSID, PASS and modules to load **here before uploading into ESP must provide the pass!!!**

### pins
- allocation pins per board. __try to keep them consistent__

### esp_lib
set of functions
- do_connect
- [ ] TODO: move out and kill file

### http_control
- control       > generic func
- pin           > trigger pin ON / OFF
                > can be used for **INTERNAL_LED**
- are_you_alive > seding reply 'I am alive' > for pinging
- cpu_freq      > change 80 / 160
- deep_sleep    > send ESP to deep sleep for N seconds
- seq           > sequential scan using one code-set with increasing the timing to find the right range.
- rf433         > control wrapper rf433
- sensor        > sensor (ADC) [currently light, but can be any]
- color         > set color of RGB LED (8 options)
- beep          > set beep pin to 1/0

### motor
- motor         > control stepper motor (with optional calibrating over lazer / light sensor)
* syntax:       http://192.168.1.175/control/motor/500/11/1
                where   500 - n steps (+/- defines direction)
                        11 - delay between steps (1/10000 sec but depends on board)
                        1 / 0 - use lazer for calibrating minimal (left / down) state

## upload.txt
syntax to upload file from CMD


## API commands / control

### RF433 MHz COMMANDS [on/off]
  * IP/conrtol/rf433/light/on
  * IP/conrtol/rf433/dimlight/on
  * IP/conrtol/rf433/coffee/on
  * IP/conrtol/rf433/heater/on
  * IP/conrtol/rf433/all/on

### OTHERS
* IP/control/are_you_alive
* IP/control/color/red
    - red / green / blue / magneta / ....
* IP/control/pin/2/1
* IP/control/beep/1
* IP/control/deep_sleep/10
    - where 10 is seconds to sleep
* IP/control/cpu_freq/80
    - 80 or 160 MHz
* IP/control/sensor
* IP/control/sensor/sound - to beep on sensing

* IP/control/motor/500/11/1
                where   500 - n steps (+/- defines direction)
                        11 - delay between steps (1/10000 sec but depends on board)
                        1 / 0 - use lazer for calibrating minimal (left / down) state
