import requests
import json
import pprint as p
import re

synced_lyrics = None
def search_songs( track_name: str, artist_name: str):
    
    api_url = "https://lrclib.net/api/search?track_name=" + track_name + "&artist_name=" + artist_name
    response = requests.get(api_url)
    
    try:
        results = response.json()
        synced: bool  = False
        if len(response.json()) < 1:
            raise Exception("Song not found") 
        for item in results:
            synced = (len(str(item["syncedLyrics"])) > 1)
            res = f"song id: {item['id']}, track name: {item['trackName']}, artist: {item['artistName']}, duration: {item['duration']},  synced lyrics: {synced}"
            print(res)

        if synced:
            synced_lyrics = 0
        if not synced:
            return None
        
    except Exception as error:
        print("Caught error: " + repr(error))
    except:
        print("Something went wrong parsing the json")
    
    return results
   
def get_lyrics(track_name: str, result_json: json):
    lyrics = None
    for result in result_json:
        lyrics = result['syncedLyrics']
        if len(lyrics) > 1:
            break
    return lyrics

def clean_lyrics(lyrics):
    cleaned_lines = []

    for line in lyrics.splitlines():
        if re.fullmatch(r'\[\d{2}:\d{2}\.\d{2}\]', line.strip()):
            continue  # skip timestamp-only lines
        
        cleaned_lines.append(line)
    return cleaned_lines

def split_time(lyrics):
    times = []
    texts = []
    json_synced = []
    data = {}
    for line in lyrics:
        if ']' in line:
            t, text = line.split(']', 1)
            time = t.strip('[')
            text = text.strip()
            times.append(time)
            texts.append(text)

            data['timestamp'] = time
            data['lyric'] = text
            json_synced.append({
                "timestamp": t.strip('['),
                "lyric": text.strip()
            })
            
    #p.pprint(json_synced)
    return json_synced

        



name   = "beat+it"
artist = "Michael+Jackson"
result = None
#result = search_songs(name,artist)
with open('test.json', encoding="utf-8") as f:
    result = json.load(f)

synced_lyrics = get_lyrics(name,result)
clean = clean_lyrics(synced_lyrics)
split_time(clean)