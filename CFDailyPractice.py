# -----------------------------------------------------------
# Jmokut's CF Daily Practice
#
# (C) 2019 Ogbonna Chibuoyim
# Email: ogbonnachibuoyim12@gmail.com
# -----------------------------------------------------------

import urllib, json, datetime, requests, math
from functools import cmp_to_key
from collections import namedtuple

POS = 1
NEG = -1
rating_dict = {}

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d.%m.%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD.MM.YYYY")

def analyze(handle, start_time):
	url = "https://codeforces.com/api/user.status?handle="+handle+"&from=1&count=30" # url is limited to 30 problems per day, increase if necessary.
	response = urllib.request.urlopen(url)
	data = json.loads(response.read()) # errors might come from here if handles are spelt incorrectly be careful!

	if(data["status"] != "OK"):
		raise SystemExit('Error: Probably bad connection or making too much requests, contact me.')	

	data = data["result"]
	problem_ratings = []
	for submission in data:
		if int(submission["creationTimeSeconds"]) >= int(start_time) and submission["verdict"] == "OK":
			problem_ratings.append(int(submission["problem"]["rating"]))

	problem_ratings.sort(reverse = True)

	return problem_ratings

def get_rating(handle):
	url = "https://codeforces.com/api/user.rating?handle="+handle
	response = urllib.request.urlopen(url)
	data = json.loads(response.read()) # errors might come from here if handles are spelt incorrectly be careful!

	if(data["status"] != "OK"):
		raise SystemExit('Error: Probably bad connection or making too much requests, contact me.')	

	data = data["result"]

	if len(data) == 0:
		return 0 # i'm using 0 for unrated users like lordvidex

	return int(data[len(data)-1]["newRating"])

Pair = namedtuple("Pair", ["first", "second"])

def formula(a, b):
	# this function continues comparing two lists 
	# to get the maximum
	# it continues taking average while there are ties 
	# it there are still ties till the end 
	# it returned the maximum of the two lists
	lista = a.first
	listb = b.first
	minlen = min(len(lista), len(listb))
	suma = lista[0] + lista[1]
	sumb = listb[0] + listb[1]
	for idx in range(2, minlen):
		suma += lista[idx]
		sumb += listb[idx]

		averagea = suma / (idx + 1)
		averageb = sumb / (idx + 1)

		scorea = averagea - rating_dict[a.second];
		scoreb = averageb - rating_dict[b.second];

		# right now some ratings can reach negative 

		if scorea < scoreb:
			return NEG
		if scorea > scoreb:
			return POS
		# function continues if they are equal

	if len(lista) > len(listb): # if ties continued just return the maximum
		return POS;
	return NEG;

def main():
	date = input("Enter date to analyze: ") # format DD.MM.YYYY
	# it analyzes from the beginning of that day and beyond 
	dt_obj = datetime.datetime.strptime(date+' 00:00:00,0',
	                           '%d.%m.%Y %H:%M:%S,%f')
	millisec = dt_obj.timestamp()

	users_list = ["fortmax120", "jmokut", "madlogic", "just_josh", "inheritag", "lordvidex"] # you can extend the list as much as you want

	for user in users_list:
		rating_dict[user] = get_rating(user)

	data = []
	for user in users_list:
		user_data = analyze(user, millisec)
		if len(user_data) >= 3: # considering only users that solved 3 or more problems
			data.append(Pair(user_data, user))

	cmp = cmp_to_key(formula) # sorts by Jmokut's formula
	data.sort(key = cmp) # at this point now results are now ready 

	for user_data in data:
		print(user_data.first) # the problem ratings 
		print(user_data.second) # the user handle
main()
