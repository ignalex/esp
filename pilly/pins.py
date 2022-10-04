# GPIO
R1          = 23
R2          = 25
R3          = 19
R4          = 18
R5          = 32

# LED
LED         = 5

# OLED DISPLAY
OLED_MOSI   = 13 #try 23
OLED_DATA   = 4
OLED_RESET  = 15
# OLED_SELECT = 2 # try without > not needed
OLED_SCK    = 14

# BTNS
B1          = 27
B2          = 33
B3          = 2
B4          = 12 # boot fail if pulled high (btns are low logic => ok)
B5          = 21
B6          = 0


# dust
DUST_LED    = 26
DUST_A      = 34


# ESP 32
# https://lastminuteengineers.com/esp32-pinout-reference/
# Label  	  GPIO  	  Safe to use?  	Reason
# D0	0	!	must be HIGH during boot and LOW for programming [ok for btn]
# TX0	1	x	Tx pin, used for flashing and debugging
# +D2	2	!	must be LOW during boot and also connected to the on-board LED [SD card MISO]
# +RX0	3	x	Rx pin, used for flashing and debugging
# +D4	4	+
# +D5	5	!	must be HIGH during boot
# D6	6	x	Connected to Flash memory
# D7	7	x	Connected to Flash memory
# D8	8	x	Connected to Flash memory
# D9	9	x	Connected to Flash memory
# D10	10	x	Connected to Flash memory
# D11	11	x	Connected to Flash memory
# +D12	12	!	must be LOW during boot
# +D13	13	+   [SD card CS]
# +D14	14	+   [SD card SCLK]
# +D15	15	!	must be HIGH during boot, prevents startup log if pulled LOW [SD card MOSI]
# RX2	16	?   doesnt work for btn
# TX2	17	?   doesnt work for btn
# +D18	18	+
# +D19	19	+
# D21	21	+ [sda for i2c] ok fir btn
# D22	22	+ [scl for i2c] not ok for btn
# +D23	23	+
# +D25	25	+
# +D26	26	+
# +D27	27	+
# +D32	32	+
# +D33	33	+
# +D34	34	!	Input only GPIO, cannot be configured as output, no pullup pulldown
# D35	35	!	Input only GPIO, cannot be configured as output, no pullup pulldown
# VP	36	!	Input only GPIO, cannot be configured as output, no pullup pulldown
# VN	39	!	Input only GPIO, cannot be configured as output, no pullup pulldown