import calc 
import datetime
import math

class Runner:
    def __init__(self, unit, dist, hrs, mins, secs):
        self.dist = calc.convert_dist_to_meters(unit, dist)
        self.time = calc.convert_time_to_mins(hrs, mins, secs)
        self.vel = self.dist/self.time #velocity in meters per minute

    def vo2max(self):
        prcntmax = .8+(0.1894393*math.exp(-0.012778*self.time))+(0.2989558*math.exp(-0.1932605*self.time)) #drop dead formula
        vo2 = -4.6+(0.182258*self.vel)+(0.000104*(self.vel**2)) #oxygen cost formula
        return int(vo2/prcntmax)

    def time_string(self):
    	return str(datetime.timedelta(minutes=self.time))


class Pace:
    def __init__(self, vo2max):
        self.vo2max = vo2max

    #effort categories and associated intensity percentage
    intensity_dict = {
    	"easy" : [.59, .74],
    	"marathon" : [.75, .84],
        "threshold" : [.82, .89], 
        "interval" : [1.00, 1.00],
        "repititions" : [1.05, 1.10]
    }

    def training_intensities(self, intensity):
    	intensity_range = self.intensity_dict[intensity]
    	pace_range = []

    	for i in range(len(intensity_range)):
    		intensity_factor = intensity_range[i]
    		velocity = calc.vo2max_to_velocity(self.vo2max*intensity_factor)
    		minutes_per_mile = round(1/(velocity/1609),1)
    		pace_range.append(str(datetime.timedelta(minutes=minutes_per_mile)))

    	return pace_range 

    def print_paces_to_terminal(self):
        easy_pace = Pace.training_intensities(self, 'easy')
        easy_pace_lower = easy_pace[1]
        easy_pace_upper = easy_pace[0]

        marathon_pace = Pace.training_intensities(self, 'marathon')
        marathon_pace_lower = marathon_pace[1]
        marathon_pace_upper = marathon_pace[0]

        threshold_pace = Pace.training_intensities(self, 'threshold')
        threshold_pace_lower = threshold_pace[1]
        threshold_pace_upper = threshold_pace[0]

        interval_pace = Pace.training_intensities(self, 'interval')
        interval_pace_lower = interval_pace[1]
        interval_pace_upper = interval_pace[0]

        repititions_pace = Pace.training_intensities(self, 'repititions')
        repititions_pace_lower = repititions_pace[1]
        repititions_pace_upper = repititions_pace[0]

        print('\n~~~~~~~~~~~~~~OUTPUT~~~~~~~~~~~~~~')
        print('\nVo2 Max: ', self.vo2max, 'mls/kg/min\n')
        print(' easy pace between: ', easy_pace_lower, 'and', easy_pace_upper, '\n')
        print(' marathon pace between: ', marathon_pace_lower, 'and', marathon_pace_upper, '\n')
        print(' threshold pace between: ', threshold_pace_lower, 'and', threshold_pace_upper, '\n')
        print(' interval pace between: ', interval_pace_lower, 'and', interval_pace_upper, '\n')
        print(' repititions pace between: ', repititions_pace_lower, 'and', repititions_pace_upper, '\n')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        return

class Program:
    def __init__(self, weeks_in, vo2max_in):
        self.weeks_in = weeks_in
        self.vo2max_in = vo2max_in

    def week(self):
        weeks = self.weeks_in
        vo2max = self.vo2max_in

        run_tuple_dict = { #week 1, week 2, week 3, week 4, repeat
        	0: ('easy', 'easy', 'easy', 'easy', 'easy', 'easy', 'rest'),
        	1: ('long', 'easy', 'easy', 'speed_1', 'easy', 'easy', 'rest'),
        	2: ('tempo', 'easy', 'easy', 'cruise_interval', 'easy', 'easy', 'rest'),
        	3: ('speed_2', 'easy', 'easy', 'speed_3', 'easy', 'easy', 'rest'),   
        	4: ('rest', 'easy', 'easy', 'easy', 'easy', 'rest', 'easy') #special for last week of training plan
        }

        consec_weeks = 0
        while weeks != 0:
            if (weeks == 1): #last week of program - KJ need to configure unique last week
                line = ['\nLast week of training', ', vo2max: ', str(vo2max), ' mls/kg/min\n\n']
                calc.print_to_plan(line)
                Program.runs(vo2max, run_tuple_dict.get(4))
                weeks = weeks-1
            else: 
                if (consec_weeks>3): #reset consecutive weeks after four week cycle
                    consec_weeks = 0
                    vo2max = vo2max+1
                line = ['\nWeek: ', str(self.weeks_in-weeks+1), ', vo2max: ', str(vo2max), ' mls/kg/min\n\n']
                calc.print_to_plan(line)
                Program.runs(vo2max, run_tuple_dict.get(consec_weeks))
                weeks = weeks-1
                consec_weeks = consec_weeks+1
        
        return

    def runs(vo2max, run_tuple):
        pace = Pace(vo2max)
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
        
        run_dict = { #add new runs here
            'easy' : ['run for 40-60 minutes between: ', easy_pace_lower, ' and ', easy_pace_upper, ' min/mile\n'],
            'rest' : ['rest day\n'],
            'long' : ['run for 13-16 miles between: ', easy_pace_lower, ' and ', easy_pace_upper, ' min/mile\n'],
            'speed_1' : ['speed work:\n', '-2 miles between: ', easy_pace_lower, ' and ', easy_pace_upper, '\n', '-3 x 1 mile at: ', threshold_pace_lower, ' with 1 minute rests\n', '-3 x 3 minutes at: ', interval_pace_upper, ' followed by 2 minutes at: ', easy_pace_upper, '\n', '-4 x 200 meters at: ', repititions_pace_upper, ' followed by 200 meters at: ', easy_pace_upper, '\n -1 mile between: ', easy_pace_lower, ' and ', easy_pace_upper, '\n'],
            'tempo' : ['tempo: 4 miles at: ', easy_pace_lower, ' followed by 7 miles at: ', marathon_pace_lower, '\n'],
            'cruise_interval' : ['cruise interval: \n-2 miles at: ', easy_pace_lower, '\n-5 miles at: ', marathon_pace_lower, '\n-1 mile at: ', easy_pace_lower, '\n-4 miles at: ', marathon_pace_lower, '\n-2 miles at: ', easy_pace_lower, '\n'],
            'speed_2' : ['speed work:\n', '-2 miles between: ', easy_pace_lower, ' and ', easy_pace_upper, '\n-5 x 1 mile at: ', threshold_pace_lower, ' with 1 minute rests\n', '-2 miles between: ', easy_pace_lower, ' and ', easy_pace_upper, '\n'],
            'speed_3' : ['speed work:\n', '-2 miles between: ', easy_pace_lower, ' and ', easy_pace_upper, '\n-5 x 1 mile at: ', threshold_pace_lower, ' with 1 minute rests\n', '-4 x 400 meters at: ', repititions_pace_upper, ' followed by 400 meters at: ', easy_pace_upper, '\n -1 mile between: ', easy_pace_lower, ' and ', easy_pace_upper, '\n']
        }

        for i in range(len(run_tuple)):
            dow = ['\t', calc.DOW_DICT.get(i), ' – ']
            calc.print_to_plan(dow)
            line = run_dict.get(run_tuple[i])
            calc.print_to_plan(line)

        return










        
        
