from classes import Runner, Pace, Program
import os

#python tool to generate a running plan based on most recent race results

#inputs
unit = 'mile'#input('\nInput unit of most recent race ran (mile or kilometer): ')
dist = 26.2#float(input('\nWhat was the distance of your latest race?: '))
hrs = 2#int(input('\nHow many hours did it take to complete you most recent race?: '))
mins = 55#int(input('\nHow many minutes did it take to complete you most recent race?: '))
secs = 34#int(input('\nHow many seconds did it take to complete you most recent race?: '))
weeks_in = 8#int(input('\nHow many weeks until your next race?: '))

#generate text file and write intro
os.remove('training_plan.txt') #remove old file before creating new
file1 = open('training_plan.txt', 'w+')
intro = ['Welcome to your marathon training plan!', '\n', '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', '\n\n']
file1.writelines(intro)
file1.close()

#main code
athlete = Runner(unit, dist, hrs, mins, secs)
Vo2Max = athlete.vo2max()
velocity = athlete.vel
time_out = athlete.time_string()
program = Program(weeks_in, Vo2Max)
program.week()

#print outro to text file
file1 = open('training_plan.txt', 'a+')
closing = ['\n\n Good luck on race day!', '\n', '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', '\n']
file1.writelines(closing)
file1.close()

#command line outputs
pace = Pace(Vo2Max)
easy_pace = pace.training_intensities('easy')
easy_pace_lower = easy_pace[1]
easy_pace_upper = easy_pace[0]

marathon_pace = pace.training_intensities('marathon')
marathon_pace_lower = marathon_pace[1]
marathon_pace_upper = marathon_pace[0]

threshold_pace = pace.training_intensities('threshold')
threshold_pace_lower = threshold_pace[1]
threshold_pace_upper = threshold_pace[0]

interval_pace = pace.training_intensities('interval')
interval_pace_lower = interval_pace[1]
interval_pace_upper = interval_pace[0]

repititions_pace = pace.training_intensities('repititions')
repititions_pace_lower = repititions_pace[1]
repititions_pace_upper = repititions_pace[0]

print('\n~~~~~~~~~~~~~~OUTPUT~~~~~~~~~~~~~~')
print('\n', dist, unit, 'race, ran in: ', time_out, '\n\n', 'Vo2 Max: ', Vo2Max, 'mls/kg/min\n')
print(' easy pace between: ', easy_pace_lower, 'and', easy_pace_upper, '\n')
print(' marathon pace between: ', marathon_pace_lower, 'and', marathon_pace_upper, '\n')
print(' threshold pace between: ', threshold_pace_lower, 'and', threshold_pace_upper, '\n')
print(' interval pace between: ', interval_pace_lower, 'and', interval_pace_upper, '\n')
print(' repititions pace between: ', repititions_pace_lower, 'and', repititions_pace_upper, '\n')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
