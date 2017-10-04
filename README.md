# ESP module control with python

## boot
1st run on start - generic

## main
2nd run on start - specific
* assign IP, SSID, PASS and modules to load **here before uploading into ESP must provide the pass!!!**

## esp_lib
set of functions
- do_connect
- blink
- get_data

## http_control1
- control       > generic func
- pin           > trigger pin ON / OFF
- are_you_alive > seding reply 'I am alive' > for pinging
- cpu_freq      > change 80 / 160
- deep_sleep    > send ESP to deep sleep for N seconds
- seq           > sequential scan using one code-set with increasing the timing to find the right range.
- rf433         > control wrapper rf433
COMMANDS [on/off]
*IP/conrtol/rf433/light/on
*IP/conrtol/rf433/dimlight/on
*IP/conrtol/rf433/coffee/on
*IP/conrtol/rf433/heater/on
*IP/conrtol/rf433/all/on



## upload.txt
syntax to upload file from CMD

## http_pins
* no idea what it was for :)

## star_wars
* socket example