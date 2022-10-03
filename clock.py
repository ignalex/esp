from machine import RTC

rtc = RTC()

# synchronize with ntp
# need to be connected to wifi
import ntptime
ntptime.settime() # set the rtc datetime from the remote server
rtc.datetime()    # get the date and time in UTC