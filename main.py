import requests
import config
import sys
from bs4 import BeautifulSoup


def get_artist_id(artist_name):

	artist_id = None
	params = {'q': artist_name}
	response = requests.get(base_url+'/search', params=params, headers=headers)
	json = response.json()

	for hit in json["response"]["hits"]:
		if (hit["result"]["primary_artist"]["name"]==artist_name) and (hit["type"]=="song"):
			artist_id = hit["result"]["primary_artist"]["id"]
			break

	if artist_id:
		print("Collecting songs for", artist_name, ": Artist ID", artist_id)
		return artist_id
	else:
		print("Artist", artist_name, "not found.")
		sys.exit(0)


def get_song_urls(artist_id):

	urls = []
	
	page_count = 1
	end_of_pages = False
	while not(end_of_pages):

		# get results of current page
		temp_url = base_url+'/artists/'+str(artist_id)+'/songs?per_page=50&page='+str(page_count)
		response = requests.get(temp_url, headers=headers)
		json = response.json()

		for song in json["response"]["songs"]:

			if song["primary_artist"]["id"]==artist_id:

				urls.append(song["path"])
		
		if json["response"]["next_page"]==None:
			end_of_pages=True
		else:
			page_count+=1

	print(len(urls), "songs found")

	return urls


def get_lyrics(song_urls):

	lyrics = []

	for url in song_urls:

		page = requests.get("https://genius.com" + url)

		if page:

			html = BeautifulSoup(page.text, "html.parser")
			[h.extract() for h in html("script")]

			text = html.find("div",class_="lyrics").get_text()
			if not text is "Lyrics will be available as soon as the song is released. Stay tuned!":
				lyrics.append(text)
				
		if len(lyrics)%100==0:
			print(len(lyrics), "/", len(song_urls), "lyrics processed")
	
	return lyrics 



if __name__ == '__main__':

	# artist input
	if len(sys.argv[1:])==0:
		print("You must pass a parameter for artist name e.g. 'Kanye West'")
		sys.exit(0)
	else:
		artist_name = sys.argv[1]

	# api key and authorisation
	base_url = "http://api.genius.com"
	api_key = config.access_token
	auth_string = 'Bearer ' + api_key
	headers = {'Authorization': auth_string}

	# get lyrics
	artist_id = get_artist_id(artist_name)
	song_urls = get_song_urls(artist_id)
	lyrics = get_lyrics(song_urls)

	# save to txt file
	if sys.argv[2]:
		filename = sys.argv[2] + ".txt"
	else:
		filename = "lyrics.txt"
	f = open(filename,"w")
	for l in lyrics:
		f.write(l)
	f.close()



