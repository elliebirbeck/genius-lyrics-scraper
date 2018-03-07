A script which works around the limitations of the [Genius API](https://docs.genius.com) to get all lyrics of an artist in one step.

- Create your own API client [here](http://genius.com/api-clients)
- Clone this repository `git clone https://github.com/elliebirbeck/genius-lyrics-scraper.git`
- Navigate to the working directory `cd genius-lyrics-scraper`
- Install dependencies `pip install -r requirements.txt`
- Create a `config.py` file with variables `client_id`, `client_secret`, `access_token` using your own API client details 

Run with the artist name as the first arg and (optionally) the filename as the second arg. E.g:

`python main.py "Amy Winehouse" "amy_lyrics"`

The sample output file `amy_lyrics.txt` is provided in the repo. It provides all songs in one file, each seperated by an `<EOS>` tag.
