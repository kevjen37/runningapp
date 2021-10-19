import math

DOW_DICT = {
	0:'Monday',
	1:'Tuesday',
	2:'Wednesday',
	3:'Thursday',
	4:'Friday',
	5:'Saturday',
	6:'Sunday'
}

def convert_time_to_mins(hrs, mins, secs):
	th = hrs*60
	tm = mins*1
	ts = secs/60
	return th+tm+ts

def convert_dist_to_meters(unit, dist):
	if (unit == 'mile'):
		return dist*1609
	if (unit == 'kilometer'):
		return dist*1000
	else:
		return dist

def vo2max_to_velocity(vo2max): 
	vel = (5.000663*vo2max) - (0.007546*vo2max**2) + 29.54
	return vel

def print_to_plan(line):     
    file1 = open('training_plan.txt', 'a+')
    file1.writelines(line)
    file1.close()
    return

