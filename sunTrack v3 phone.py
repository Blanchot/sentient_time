# 28.02.2018
# PHONE version with Notifications
# Breaking out a while loop (if button taking too long to respond) type: ;;

import time
import datetime
from datetime import timedelta
from dateutil.relativedelta import *
import requests, json
import notification
import sound

#--- GET THE USNO DATA FOR TODAY---#
now = datetime.datetime.now()
urlDate = now.strftime("%m/%d/%Y") #USNO only needs day, month, year and location
# NOTE: standard tz at end of line below is tz=1. Summer time is tz=2! 
usno = 'http://api.usno.navy.mil/rstt/oneday?date=' + urlDate +'&coords=51.54N,4.30E&tz=2'
# Get USNO json file via requests
usnoData = requests.get(usno).json()
# Create date string for creating datetime objects below
dateStr = now.strftime("%Y-%m-%d")


#--- PARSE THE USNO DATA AND CREATE DATETIME.DATIME OBJECTS FOR TODAY'S EVENTS---#
beginCivilTwilight = usnoData['sundata'][0]['time']
BCT = datetime.datetime.strptime(dateStr + ' ' + beginCivilTwilight, '%Y-%m-%d %H:%M')

sunrise = usnoData['sundata'][1]['time']
sR = datetime.datetime.strptime(dateStr + ' ' + sunrise, '%Y-%m-%d %H:%M')

upperTransit_S = usnoData['sundata'][2]['time']
uS = datetime.datetime.strptime(dateStr + ' ' + upperTransit_S, '%Y-%m-%d %H:%M')

sunset = usnoData['sundata'][3]['time']
sS = datetime.datetime.strptime(dateStr + ' ' + sunset, '%Y-%m-%d %H:%M')

endCivilTwilight = usnoData['sundata'][4]['time']
ECT = datetime.datetime.strptime(dateStr + ' ' + endCivilTwilight, '%Y-%m-%d %H:%M')

print('USN0 DATA FOR TODAY')
print('='*19)
print (now.strftime("%Y-%m-%d %H:%M:%S") + ' (polling time)')
#print(str(BCT) + ' (BCT: begin civil twilight)')
#print(str(sR) + ' (sR: sunrise)')
#print(str(uS) + ' (uS: upper transit sun)')
#print(str(sS) + ' (sS: sunset)')
#print(str(ECT) + ' (ECT: end civil twilight)')
#print()

#--- GET THE USNO DATA FOR TOMORROW---#
#To calculate the night kaspu starting from ECT tonight to BCT tomorrow
now = datetime.datetime.now()
tomorrow = now + relativedelta(days=+1)

urlDateTomorrow = tomorrow.strftime("%m/%d/%Y")
usnoTomorrow='http://api.usno.navy.mil/rstt/oneday?date=' + urlDateTomorrow +'&coords=51.54N,4.30E&tz=1'
# Get USNO for TOMORROW json file via requests
usnoTomorrowData = requests.get(usnoTomorrow).json()
# Create date string for creating TOMORROW'S BCT datetime object below
dateStrTomorrow = tomorrow.strftime("%Y-%m-%d")

endOfNight = usnoTomorrowData['sundata'][0]['time']
EON = datetime.datetime.strptime(dateStrTomorrow + ' ' + endOfNight, '%Y-%m-%d %H:%M')


#--- CALCULATING DAYLIGHT: THE TIMEDIFF FUNCTION ---#
# dateutil.relativedelta(datetime_obj2, datetime_obj1)

def timeDiff(datetime_obj2, datetime_obj1):
	diff = relativedelta(datetime_obj2, datetime_obj1)
	diffString = (str(diff.hours) + ' hrs, ' + str(diff.minutes) + ' mins')
	return diffString

print('Daylight: ' + timeDiff(ECT,BCT))

#--- CALCULATING THE DAY KASPU ---#

def calcDayKaspu(datetime_obj2, datetime_obj1):
	delta_obj = datetime_obj2 - datetime_obj1
	kaspuSecs = delta_obj.seconds // 6 # this is the kaspu seconds as int
	kaspuDelta_obj = delta_obj / 6 # kaspuDelta_obj is a datetime.timedelta object
	kaspuString = str(timedelta(seconds=kaspuDelta_obj.seconds))
	print(' Light kaspu: '+ str(kaspuSecs) + ' secs OR ' + kaspuString)
	return kaspuDelta_obj

dayKaspu = calcDayKaspu(ECT,BCT) #dayKaspu as a timedelta object

def calcNightKaspu(datetime_obj2, datetime_obj1):
	delta_obj = datetime_obj2 - datetime_obj1
	kaspuSecs = delta_obj.seconds // 6 # this is the kaspu seconds as int
	kaspuDelta_obj = delta_obj / 6 # kaspuDelta_obj is a datetime.timedelta object
	kaspuString = str(timedelta(seconds=kaspuDelta_obj.seconds))
	print('  Dark kaspu: '+ str(kaspuSecs) + ' secs OR ' + kaspuString)
	return kaspuDelta_obj

nightKaspu = calcNightKaspu(EON,ECT) #dayKaspu as a timedelta object

kaspu_01 = BCT
kaspu_02 = BCT + dayKaspu
kaspu_03 = BCT + (dayKaspu *2)
kaspu_04 = BCT + (dayKaspu *3)
kaspu_05 = BCT + (dayKaspu *4)
kaspu_06 = BCT + (dayKaspu *5)

kaspu_07 = ECT
kaspu_08 = ECT + nightKaspu
kaspu_09 = ECT + (nightKaspu *2)
kaspu_10 = ECT + (nightKaspu *3)
kaspu_11 = ECT + (nightKaspu *4)
kaspu_12 = ECT + (nightKaspu *5)

print()
print('KASPU TIMES')
print('='*12)
print('01: ' +str(kaspu_01.time()) + '  Rabbit-BCT')
print(' '*14 + 'Sunrise: ' + str(sR.time()))
print('02: ' +str(kaspu_02.time()) + '  Dragon')
print('03: ' +str(kaspu_03.time()) + '  Snake')
print(' '*14 + 'High noon: ' + str(uS.time()))
print('04: ' +str(kaspu_04.time()) + '  Horse')
print('05: ' +str(kaspu_05.time()) + '  Goat')
print('06: ' +str(kaspu_06.time()) + '  Monkey')
print(' '*14 + 'Sunset: ' + str(sS.time()))
#print()
print('07: '	+str(kaspu_07.time()) + '  Rooster-ECT')
print('08: '	+str(kaspu_08.time()) + '  Dog')
print('09: '	+str(kaspu_09.time()) + '  Pig')
print('10: '	+str(kaspu_10.time()) + '  Rat')
print('11: '	+str(kaspu_11.time()) + '  Ox')
print('12: '	+str(kaspu_12.time()) + '  Tiger')

print('='*12)
print()

#--- NOTIFICATION SETUP ---#
#notification.get_scheduled()
#notification.cancel(notification)

notification.cancel_all()

def secsFromNow(datetime_obj): #datetime_obj is kaspu_xx
	now = datetime.datetime.now()
	timedelta = datetime_obj - now #produces a timedelta object
	delay = timedelta.seconds #the required number of seconds until the notification event
	return delay

def notifyKaspu():
	now = datetime.datetime.now()
	if now < kaspu_01:
		k1Str = 'Kaspu 01 Rabbit: ' +str(kaspu_01.time())
		notification.schedule(k1Str, delay=secsFromNow(kaspu_01),sound_name='Media/Sounds/piano/G4#')
	if now < kaspu_02:
		k2Str = 'Kaspu 02 Dragon: ' +str(kaspu_02.time())
		notification.schedule(k2Str, delay=secsFromNow(kaspu_02),sound_name='Media/Sounds/piano/G4')
	if now < kaspu_03:
		k3Str = 'Kaspu 03 Snake: ' +str(kaspu_03.time())
		notification.schedule(k3Str, delay=secsFromNow(kaspu_03),sound_name='Media/Sounds/piano/F4#')
	if now < kaspu_04:
		k4Str = 'Kaspu 04 Horse: ' +str(kaspu_04.time())
		notification.schedule(k4Str, delay=secsFromNow(kaspu_04),sound_name='Media/Sounds/piano/F4')
	if now < kaspu_05:
		k5Str = 'Kaspu 05 Goat: ' +str(kaspu_05.time())
		notification.schedule(k5Str, delay=secsFromNow(kaspu_05),sound_name='Media/Sounds/piano/E4')
	if now < kaspu_06:
		k6Str = 'Kaspu 06 Monkey: ' +str(kaspu_06.time())
		notification.schedule(k6Str, delay=secsFromNow(kaspu_06),sound_name='Media/Sounds/piano/D4#')
	if now < kaspu_07:
		k7Str = 'Kaspu 07 Rooster: ' +str(kaspu_07.time())
		notification.schedule(k7Str, delay=secsFromNow(kaspu_07),sound_name='Media/Sounds/piano/D4')
	if now < kaspu_08:
		k8Str = 'Kaspu 08 Dog: ' +str(kaspu_08.time())
		notification.schedule(k8Str, delay=secsFromNow(kaspu_08),sound_name='Media/Sounds/piano/C4#')
	if now < kaspu_09:
		k9Str = 'Kaspu 09 Pig: ' +str(kaspu_09.time())
		notification.schedule(k9Str, delay=secsFromNow(kaspu_09),sound_name='Media/Sounds/piano/C4')
	if now < kaspu_10:
		k10Str = 'Kaspu 10 Rat: ' +str(kaspu_10.time())
		notification.schedule(k10Str, delay=secsFromNow(kaspu_10),sound_name='Media/Sounds/piano/B3')
	if now < kaspu_11:
		k11Str = 'Kaspu 11 Ox: ' +str(kaspu_11.time())
		notification.schedule(k11Str, delay=secsFromNow(kaspu_11),sound_name='Media/Sounds/piano/A3#')
	if now < kaspu_12:
		k12Str = 'Kaspu 12 Tiger: ' +str(kaspu_12.time())
		notification.schedule(k12Str, delay=secsFromNow(kaspu_12),sound_name='Media/Sounds/piano/A3')

notifyKaspu()

def printNots():
	notsList = notification.get_scheduled()
	for i in range(len(notsList)):
		print(notsList[i])
		print()

# printNots()

'''
#--- CONSOLE TIMER SECTION WHILE LOOP---#

k01 = False
k02 = False
k03 = False
k04 = False
k05 = False
k06 = False
k07 = False
k08 = False
k09 = False
k10 = False
k11 = False
k12 = False

while True:
	now = datetime.datetime.now()
	if now > kaspu_01 and k01 == False:
		k01 = True
		G4s = sound.Player('piano:G4#')
		G4s.play()
		print ('Kaspu 01 has begun')
	elif now > kaspu_02 and k02 == False:
		k02 = True
		G4 = sound.Player('piano:G4')
		G4.play()
		print ('Kaspu 02 has begun')
	elif now > kaspu_03 and k03 == False:
		k03 = True
		F4s = sound.Player('piano:F4#')
		F4s.play()
		print ('Kaspu 03 has begun')
	elif now > kaspu_04 and k04 == False:
		k04 = True
		F4 = sound.Player('piano:F4')
		F4.play()
		print ('Kaspu 04 has begun')
	elif now > kaspu_05 and k05 == False:
		k05 = True
		E4 = sound.Player('piano:E4')
		E4.play()
		print ('Kaspu 05 has begun')
	elif now > kaspu_06 and k06 == False:
		k06 = True
		D4s = sound.Player('piano:D4#')
		D4s.play()
		print ('Kaspu 06 has begun')
	elif now > kaspu_07 and k07 == False:
		k07 = True
		print ('Kaspu 07 has begun')
	elif now > kaspu_08 and k08 == False:
		k08 = True
		print ('Kaspu 08 has begun')
	elif now > kaspu_09 and k09 == False:
		k09 = True
		print ('Kaspu 09 has begun')
	elif now > kaspu_10 and k10 == False:
		k10 = True
		print ('Kaspu 10 has begun')
	elif now > kaspu_11 and k11 == False:
		k11 = True
		print ('Kaspu 11 has begun')
	elif now > kaspu_12 and k12 == False:
		k12 = True
		print ('Kaspu 12 has begun')
	time.sleep(10)


'''

'''
1.0, .82, .17
1.0, 1.0, 1.0

import notification

notification.schedule('Test', delay=5, sound_name='Media/Sounds/drums/Drums_15')
The same pattern ('Media/Sounds/<collection>/<name>') should work with any of the bundled sounds, not just the 'digital' and 'game' collections.

import sound
# Play the result:
player = sound.MIDIPlayer('output.mid')
sound.Player(file_path)
player.play()

'''
