import time
import os
import serial
import math
from datetime import date
from datetime import datetime

print("////////////////////////////////")
print("//////// OAT Config V0.1 ///////")
print("////////////////////////////////")
print("////////////////////////////////")
print("/// Set RA and DEC wheels to ///")
print("/// home possitions and plug ///")
print("/// USB cable to Astroberry  ///")
print("/// ls /dev/tty* on other    ///")
print("/// terminal to find port    ///")
print("////////////////////////////////")

#//////////////////////////////////////////////////////
# set serial port & disable reset on port open
# otherwise OAT will forget time&date when KSTARS connects
#/////////////////////////////////////////////////////

isport = input("Is OAT at /dev/ttyUSB0? (y/n): ")

if  (isport) == ("n"):
    serialport = input("What port OAT is using?: ")
    print("COM port set to " + serialport)
    print("Disabling #DTR for " + serialport)
    #os.system('stty -F ' + serialport + ' -hupcl')
        
else:
    print("COM port set to /dev/ttyUSB0")
    print("Disabling #DTR for /dev/ttyUSB0")
    serialport = "/dev/ttyUSB0"
    #os.system('stty -F /dev/ttyUSB0 -hupcl')


#////////////////////////////////////
# open serial port & check connection
#///////////////////////////////////


print("Opening serial port on " + serialport + '...')
ser = serial.Serial(serialport, 19200, timeout = 1)
time.sleep(5)                                           #wait for reboot
ser.write(str.encode(':GVP#:GVN#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))

if (response_utf) == ('') :
    print('Could not communicate with OAT, quitting...')
    quit()

else:  print(str(response_utf) + ' is online!') 

#////////////////////////////////////
# Try enabling level and read values
#///////////////////////////////////

ser.write(str.encode(':XL1#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))


if  (response_utf) == ("1#"):
    levelread = input("Start reading Digital Level? (y/n): ")
    if (levelread) == ("y"):
        print('Press CTRL+C to stop...')
        try:
            while True:
                pass 
                ser.write(str.encode(':XLGC#'))
                response = ser.readline()
                response_utf = (response.decode('utf-8'))
                print(response_utf)
                time.sleep(1)
        except KeyboardInterrupt:
                pass
                ser.write(str.encode(':XL0#'))                
                response = ser.readline()
                response_utf = (response.decode('utf-8'))
                if (response_utf) == ('1#') :
                        print('Disabbling digital level...')
                else:   print('Could not dissable digital level') 

else: print('Digital level not installed...')


#////////////////////////////////////
# Set site coordinates
#///////////////////////////////////

iscord = input("Set site coordinates to Home? (y/n): ")

if  (iscord) == ("n"):
    print('All coordinates are in DM (DegreesMinutes) format!')
    LAT = input ("Enter Site LAT DD*MM: ")
    
    if int(LAT.split('*')[0]) >= 0 :
        LAT_SIGN = ('+' + str(LAT))
    else:  LAT_SIGN = LAT

    LONG = input ("Enter Site LONG DD*MM: ")
    LONG_DEG = LONG.split('*')[0]
    LONG_MIN = LONG.split('*')[1]
    LONG_CONV = math.modf((10800 - ((int(LONG_DEG) * 60.0) + int(LONG_MIN)))/60) 

    LONG_CONV_DEG = (int(LONG_CONV[1]))
    LONG_CONV_DEG_STR = str(LONG_CONV_DEG)
    LONG_CONV_DEG_ZERO = LONG_CONV_DEG_STR.zfill(3)
    LONG_CONV_MIN_CAL = int((LONG_CONV[0]) * 60)
    LONG_CONV_MIN_CAL_STR = str(LONG_CONV_MIN_CAL)
    LONG_CONV_MIN_CAL_ZERO = LONG_CONV_MIN_CAL_STR.zfill(2)
   
    LONGABS = str(LONG_CONV_DEG_ZERO) + '*' + str(LONG_CONV_MIN_CAL_ZERO)
    #print(LONGABS)
    #print(LAT_SIGN)

else:

    print("Home Site LAT is 01*01")     # Show your Home Latitude in DM (DegreesMinutes) format
    LAT_SIGN = "+01*01"                 # Enter your Latitude + for northern Hemisphere - for South
    LONG = "01*01"                      # Enter your Longitude in DM (DegreesMinutes) format
    LONG_DEG = LONG.split('*')[0]
    LONG_MIN = LONG.split('*')[1]
    LONG_CONV = math.modf((10800 - ((int(LONG_DEG) * 60.0) + int(LONG_MIN)))/60) 

    LONG_CONV_DEG = (int(LONG_CONV[1]))
    LONG_CONV_DEG_STR = str(LONG_CONV_DEG)
    LONG_CONV_DEG_ZERO = LONG_CONV_DEG_STR.zfill(3)
    LONG_CONV_MIN_CAL = int((LONG_CONV[0]) * 60)
    LONG_CONV_MIN_CAL_STR = str(LONG_CONV_MIN_CAL)
    LONG_CONV_MIN_CAL_ZERO = LONG_CONV_MIN_CAL_STR.zfill(2)
   
    LONGABS = str(LONG_CONV_DEG_ZERO) + '*' + str(LONG_CONV_MIN_CAL_ZERO) # 180deg 00min 'minus' your LONG if positive or 'plus' if negative 
    
    print("Home Site LONG is: " + str(LONGABS))    # Show your Home Longitude       
                                        

ser.write(str.encode(':St' + str(LAT_SIGN) + '#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('Latitude successfully set to: ' + str(LAT_SIGN))
else: print('Could not set Latitude...')

ser.write(str.encode(':Sg' + str(LONGABS) + '#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('Longitude successfully set to: ' + str(LONGABS))
else: print('Could not set Longitude...')


#////////////////////////////////////
# Set Time
#///////////////////////////////////

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
#print("Current Time =", current_time)

ser.write(str.encode(':SL' + str(current_time) + '#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('Site local time successfully set to: ' + str(current_time))
else: print('Could not set local time...')

#////////////////////////////////////
# Set Date
#///////////////////////////////////

today = date.today()

# mm/dd/y
d3 = today.strftime("%m/%d/%y")
#print("Current Date =", d3)

ser.write(str.encode(':SC' + str(d3) + '#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))
response_set = (''.join(filter(str.isdigit, response_utf)))
if int(response_set) == 1:
    print('Site date successfully set to: ' + str(d3))
    response_strip = response_utf.strip("1")
    print(str(response_strip) + ' done!') 
else: print('Could not set site date...')



#////////////////////////////////////
# Set UTC Offset
#///////////////////////////////////

ts = time.time()
utc_offset = (datetime.fromtimestamp(ts) -
              datetime.utcfromtimestamp(ts)).total_seconds()

utc_offset_hour = int(utc_offset / 3600)

if  utc_offset_hour > 0:
    utc_offset_hour_str = str(utc_offset_hour)
    utc_offset_hour_zero = utc_offset_hour_str.zfill(2)
    utc_offset_hour_sign = '+' + str(utc_offset_hour_zero)
elif  utc_offset_hour < 0:
    utc_offset_hour_str = str(abs(utc_offset_hour))
    utc_offset_hour_zero = utc_offset_hour_str.zfill(2)
    utc_offset_hour_sign = '-' + str(utc_offset_hour_zero)
else:
    utc_offset_hour_sign = str('+00')


ser.write(str.encode(':SG' + str(utc_offset_hour_sign) + '#'))
response = ser.readline()
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('Site UTC offset successfully set to: ' + str(utc_offset_hour_sign))
else: print('Could not set UTC offset...')
#print("Current UTC offset =", utc_offset_hour_sign)


#////////////////////////////////////
# Try AutoHome RA
#///////////////////////////////////

print('Traying to Home RA using Hall sensor...')
ser.timeout = None #Let's wait for Autohoming to finish
ser.write(str.encode(':MHRR#'))
response = ser.read(1)
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('RA successfully Homed!')
else: print('Could not Auto Home or not installed...')


#////////////////////////////////////
# Set current position as Home
#///////////////////////////////////
print('Setting current orientation as Home Point')
ser.timeout = None
ser.write(str.encode(':SHP#'))
response = ser.read(1)
response_utf = (response.decode('utf-8'))
if int(response_utf) == 1:
    print('Done!')
else: print('Could not set Home Point...')


#////////////////////////////////////
# Stop and exit
#///////////////////////////////////
#print('Stoping all motors...')
#ser.write(str.encode(':Q#'))

ser.close() 

print("////////////////////////////////")
print("/// OAT configuration is     ///")
print("/// completed. Disable Time  ///")
print("/// and Location updating    ///")
print("/// in KSTARS before         ///")
print("/// connecting to OAT!!!     ///")
print("////////////////////////////////")