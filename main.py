import requests
import config
import sys
import requests
from bs4 import BeautifulSoup

def html_parser(url):
    try :

        response = requests.get("https://genius.com" + url)
        response.raise_for_status()  # Check for request errors

        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all <div> tags where the class starts with "Lyrics__Container"
        lyrics_containers = soup.select('div[class^="Lyrics__Container"]')

        lyrics_text = []
        for container in lyrics_containers:
            lyrics_text.append(container.get_text(separator="\n", strip=True))

        full_lyrics = "\n".join(lyrics_text)

        return full_lyrics
    except Exception as e :
        print(e)
        return ""

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

if __name__ == '__main__':

	# artist input
	if len(sys.argv[1:])==0:
		print("You must pass a parameter for artist name e.g. \"Kanye West\"")
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

	urls = []
	page_count = 1	
	end_of_pages = False

	if len(sys.argv)>2:
		filename = sys.argv[2] + ".txt"
	else:
		filename = "lyrics.txt"

	while not(end_of_pages):

		# get results of current page
		temp_url = base_url+'/artists/'+str(artist_id)+'/songs?per_page=50&page='+str(page_count)
		response = requests.get(temp_url, headers=headers)
		json = response.json()

		for song in json["response"]["songs"]:

			if song["primary_artist"]["id"]==artist_id:

				urls.append(song["path"])
				text = html_parser(song["path"])

				if "Lyrics will be available" not in text:

					f = open(filename,"a")
					f.write(text + "\n\n")
					f.close()
					
		if json["response"]["next_page"]==None:
			end_of_pages=True
		else:
			page_count+=1

	print(len(urls), "songs found")
	print("File saved at",filename)



