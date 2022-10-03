from machine import Pin, SoftSPIimport sh1106def oled_spi(mosi=13, data=4, reset=15, select=2, sck=14, intro = 'HELLO :)', rotate = 0):    spi = SoftSPI(baudrate=500000, polarity=1, phase=0, sck=Pin(sck), mosi=Pin(mosi), miso=Pin(12))    display = sh1106.SH1106_SPI(128, 64, spi, Pin(data), Pin(reset), Pin(select) if select is not None else None, rotate)    display.sleep(False)    display.fill(0)    display.text(intro, 0, 0, 1)    display.show()    return display# ---basic# display.poweroff()     # power off the display, pixels persist in memory# display.poweron()      # power on the display, pixels redrawn# display.contrast(0)    # dim# display.contrast(255)  # bright# display.invert(1)      # display inverted# display.invert(0)      # display normal# display.rotate(True)   # rotate 180 degrees# display.rotate(False)  # rotate 0 degrees# display.show()         # write the contents of the FrameBuffer to display memory# ---graphic# display.fill(0)                         # fill entire screen with colour=0# display.pixel(0, 10)                    # get pixel at x=0, y=10# display.pixel(0, 10, 1)                 # set pixel at x=0, y=10 to colour=1# display.hline(0, 8, 4, 1)               # draw horizontal line x=0, y=8, width=4, colour=1# display.vline(0, 8, 4, 1)               # draw vertical line x=0, y=8, height=4, colour=1# display.line(0, 0, 127, 63, 1)          # draw a line from 0,0 to 127,63# display.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1# display.fill_rect(10, 10, 107, 43, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1# display.text('Hello World', 0, 0, 1)    # draw some text at x=0, y=0, colour=1# display.scroll(20, 0)                   # scroll 20 pixels to the right# # draw another FrameBuffer on top of the current one at the given coordinates# import framebuf# fbuf = framebuf.FrameBuffer(bytearray(8 * 8 * 1), 8, 8, framebuf.MONO_VLSB)# fbuf.line(0, 0, 7, 7, 1)# display.blit(fbuf, 10, 10, 0)           # draw on top at x=10, y=10, key=0# display.show()