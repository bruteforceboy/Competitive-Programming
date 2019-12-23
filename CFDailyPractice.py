# -----------------------------------------------------------
# Jmokut's CF Daily Practice
# 
# (C) 2019 Ogbonna Chibuoyim
# Email: ogbonnachibuoyim12@gmail.com
# 
# Python 3.7.3
# -----------------------------------------------------------

import urllib, json, datetime, requests, math
from functools import cmp_to_key
from collections import namedtuple

POS = 1
NEG = -1
rating_dict = {}

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d.%m.%Y %H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD.MM.YYYY HH:MM:SS")

def analyze(handle, start_time, end_time):
	url = "https://codeforces.com/api/user.status?handle="+handle+"&from=1&count=30" # url is limited to 30 problems per day, increase if necessary.
	response = urllib.request.urlopen(url)
	data = json.loads(response.read()) # errors might come from here if handles are spelt incorrectly be careful!

	if(data["status"] != "OK"):
		raise SystemExit('Error: Probably bad connection or making too much requests, contact me.')	

	data = data["result"]
	problem_ratings = []
	for submission in data:
		if int(submission["creationTimeSeconds"]) >= int(start_time) and int(submission["creationTimeSeconds"]) <= end_time and submission["verdict"] == "OK":
			if "rating" not in submission["problem"]:
				continue
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
		return 0 # unrated users like lordvidex

	return int(data[len(data)-1]["newRating"])

Pair = namedtuple("Pair", ["first", "second"])

def formula(a, b):
	# this function continues comparing two lists 
	# to get the maximum
	# it continues taking average while there are ties 
	# it there are still ties till the end 
	# it will return the maximum of the two lists
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

		if scorea < scoreb:
			return POS
		if scorea > scoreb:
			return NEG
		
	if len(lista) > len(listb): # if tied continued just return the maximum
		return NEG
	return POS

def lower_than_rating(data, handle):
	rating = rating_dict[handle]
	expected = (rating + 100) / 100
	expected = int(expected) * 100 # expected is next closest integer divisible by 100 
	max_average = (data[0] + data[1] + data[2]) / 3
	if max_average < expected:
		return 1
	return 0

def score(data, user):
	return int((data[0] + data[1] + data[3]) / 3) - rating_dict[user]

def main():
	print("------------------------------------------------------------------------\n")
	print("JMOKUT'S CODEFORCES DAILY PRACTICE TOOL.\n")
	print("Enter START datetime and END datetime to begin analyzing\n")

	beg_datetime = input("Enter start datetime (DD.MM.YYYY HH:MM:SS) : ") # format DD.MM.YYYY HH:MM:SS
	validate(beg_datetime)
	end_datetime = input("Enter ending datetime (DD.MM.YYYY HH:MM:SS) : ") # format DD.MM.YYYY HH:MM:SS
	validate(end_datetime)

	# CF uses milliseconds for time analysis
	beg_obj = datetime.datetime.strptime(beg_datetime+',0',
	                           '%d.%m.%Y %H:%M:%S,%f')
	end_obj = datetime.datetime.strptime(end_datetime+',0',
							   '%d.%m.%Y %H:%M:%S,%f')

	beg_millisec = beg_obj.timestamp()
	end_millisec = end_obj.timestamp()

	users_list = ["fortmax120", "jmokut", "madlogic", "just_josh", "inheritag", "lordvidex", "tourist"] # you can extend the list as much as you want

	print("\nGetting user ratings...\n")
	for user in users_list:
		rating_dict[user] = get_rating(user)
		if rating_dict[user] == 0:
			print("[contestant] " + user + " is unrated (using 1200 as default rating), beware\n")
			rating_dict[user] = 1200

	print("Analyzing problems solved by users...\n")
	data = []
	for user in users_list:
		user_data = analyze(user, beg_millisec, end_millisec)
		if len(user_data) < 3:
			print("[contestant] " + user + " solved " + str(len(user_data)) + " problems not upto 3\n");
		elif lower_than_rating(user_data, user) == 1:
			print("[contestant] " + user + " solved easier problems than his current rating\n")
		else:
			data.append(Pair(user_data, user))

	cmp = cmp_to_key(formula) # sorts by Jmokut's formula
	data.sort(key = cmp) # at this point now results are now ready 

	print("\n")
	rank = 1
	for user_data in data:
		print("RANK " + str(rank) + " [contestant] " + user_data.second + " [score]: " + str(score(user_data.first, user_data.second)))
		rank = rank + 1

	print("\n\nDONE.")
	print("------------------------------------------------------------------------\n")

main()
