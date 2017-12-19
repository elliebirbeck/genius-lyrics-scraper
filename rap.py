import requests
import config
from bs4 import BeautifulSoup

# api key and authorisation

base_url = "http://api.genius.com"
api_key = config.access_token
auth_string = 'Bearer ' + api_key
headers = {'Authorization': auth_string}

# get artist id
artist_name = "Kanye West"
artist_id = None
params = {'q': artist_name}
search_url = base_url + "/search"
response = requests.get(search_url, params=params, headers=headers)
json = response.json()

for hit in json["response"]["hits"]:
	if (hit["result"]["primary_artist"]["name"]==artist_name):
		artist_id = hit["result"]["primary_artist"]["id"]
		print("Name:\t", artist_name)
		print("ID:\t", artist_id)
		break


# loop through all results of api request returns
page_count = 1
end_of_pages = False
while not(end_of_pages):

	# get results of current page
	temp_url = base_url+'/artists/'+str(artist_id)+'/songs?per_page=50&page='+str(page_count)
	response = requests.get(temp_url, headers=headers)
	json = response.json()

	for song in json["response"]["songs"]:

		# check for only primary artist
		if song["primary_artist"]["id"]==artist_id:
			print(song["full_title"])
	

	if json["response"]["next_page"]==None:
		end_of_pages=True
	else:
		page_count+=1


