import requests
import urllib3
import datetime
from time import mktime
from statistics import mean
from classes import Runner, Pace
import calc

def Strava_Vo2():

	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

	auth_url = "https://www.strava.com/oauth/token"
	activites_url = "https://www.strava.com/api/v3/athlete/activities"
	split_activites_url = "https://www.strava.com/api/v3/activities"

	now = datetime.datetime.now()
	then = now - datetime.timedelta(days=10) #change number if returning key error
	earlier_time = int(mktime(then.timetuple())) #only return runs from 20 days and sooner – Strava doesn't allow more than 20

	athlete_name = 'kevin'#input('\nAthlete Name: ')

	athlete_dict = {
		'kevin' : '1', #fake API token
		'vicki' : '2', #fake API token
		'brandon' : '3' #fake API token
	}

	athlete_token = athlete_dict[athlete_name]

	payload = {
    	'client_id': "66642",
    	'client_secret': 'bfac709db726163c51137267d35f085e7f22953a',
    	'refresh_token': athlete_token,
    	'grant_type': "refresh_token",
    	'f': 'json'
	}

	print("Requesting Token...\n")
	res = requests.post(auth_url, data=payload, verify=False)
	access_token = res.json()['access_token']
	print(athlete_name, "access token = {}\n".format(access_token))

	print("Analyzing Strava Data...\n")

	header = {'Authorization': 'Bearer ' + access_token}
	param = {'per_page': 200, 'page': 1, 'after' : earlier_time}

	my_dataset = requests.get(activites_url, headers=header, params=param).json()

	activity_ids = [] #search for run activities with achievements
	for i in range(len(my_dataset)):
		if (my_dataset[i]["type"] == 'Run'): #and (my_dataset[i]["achievement_count"] > 0)): 
			activity_ids.append(my_dataset[i]["id"])

	vo2_list = []
	splits_list = []
	MaxVo2Max = 0
	for i in range(len(activity_ids)): #use activities with achievements as activities to search for high Vo2Max
		param_splits = {'id' : activity_ids[i]}
		split_dataset = requests.get(split_activites_url + '/' + str(activity_ids[i]) + '?include_all_efforts', headers=header, params=param_splits).json()
		run_total_km = len(split_dataset['splits_metric'])
		#iterate through splits, calculate Vo2 max from every subset and add to Vo2 max list
		for x in range(run_total_km): 
			splits_list.clear()
			distance_km = 0
			for y in range(x, run_total_km):
				if (split_dataset['splits_metric'][y]['distance'] > 950): #exclude splits that are less than 990 meters (otherwise not a complete 1km split)
					splits_list.append(split_dataset['splits_metric'][y]['moving_time'])
					distance_km = distance_km+1
					if (distance_km>=5): #calculate vo2 max using 5k minimum
						split_average = sum(splits_list)
						athlete = Runner('kilometer', distance_km, 0, 0, split_average)
						Vo2Max = athlete.vo2max()
						time = athlete.time_string()
						vo2_list.append(Vo2Max)
			if (max(vo2_list)>MaxVo2Max):
				MaxVo2Max = max(vo2_list)

	pace = Pace(MaxVo2Max)
	pace.print_paces_to_terminal()
	return MaxVo2Max

