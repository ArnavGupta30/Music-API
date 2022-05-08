from youtube_search import YoutubeSearch
from spotify import SpotifyAPI
import re
import pafy
# import requests
''' do not do pip install pafy, do - pip install -e git+git://github.com/mohamed-challal/pafy.git@develop#egg=pafy '''
client_id = '574113ae79c246db956bfc33471fdf0d'
client_secret = '60c1057e87c14c7595044d7a0a51be51'
spotify = SpotifyAPI(client_id, client_secret)

def search(query):
	results = spotify.search(query)
	result_length = len(results['tracks']['items'])
	if result_length == 0:
		pass
	else:
		unsorted_search_results = []
		popularity_index = []
		count = 0
		for result in range(result_length):
			song = results['tracks']['items'][result]['name']
			artist = results['tracks']['items'][result]['album']['artists'][0]['name']
			popularity = results['tracks']['items'][result]['popularity']
			re_string = f"/{song}{artist.title()}"
			redirect = re.sub('[^A-Za-z0-9]+', '', re_string.lower())
			popularity_index.append(popularity)
			unsorted_search_results.append({
				'name': f"{song} - {artist.title()}",
				'popularity': int(popularity)}
			)
			count += 1
	search_results = []
	for x in popularity_index:
		max_index = popularity_index.index(max(popularity_index))
		search_results.insert(-1, unsorted_search_results[max_index])
		popularity_index.pop(max_index)
		unsorted_search_results.pop(max_index)
	top_song = search_results.pop()
	search_results.insert(0, top_song)
	return search_results
		
def geturl(query):
	data = YoutubeSearch(query, max_results=1).to_dict()
	id = data[0]['id']
	url = "www.youtube.com/watch?v=" + id
	audio = pafy.new(url).getbestaudio().url
    # try:
	# 	requests.get(audio)
	# except requests.ConnectionError or urllib3.exceptions.LocationParseError or requests.exceptions.InvalidURL or requests.exceptions.MissingSchema:
	# 	return "The selected song can't be played at the moment"
	result = {"audio" : audio, "info": data[0]}
	return result