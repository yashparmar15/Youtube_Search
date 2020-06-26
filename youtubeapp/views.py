import requests

from django.conf import settings
from django.shortcuts import render

from isodate import parse_duration 

def index(request):
    videos = []
    if request.method == "POST":
        youtube_search_url = 'https://www.googleapis.com/youtube/v3/search'
        youtube_video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part' : 'snippet',
            'q' : request.POST['name'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 12,
            'type' : 'vedio',
        }
        ids = []
        data = requests.get(youtube_search_url, params = search_params)
        results = data.json()['items']
        for result in results:
            a = result['id']['kind']
            if a == "youtube#video":
                ids.append(result['id']['videoId'])


        vedio_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(ids),
            'maxResults' : 20,
        }
        data = requests.get(youtube_video_url,params = vedio_params)
        
        results = data.json()['items']
        for result in results:
            vedio_data = {
                'title' : result['snippet']['title'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'id' : result['id'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60 + 1),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'publish' : result['snippet']['publishedAt']    
            }
            videos.append(vedio_data)
    context = {
        'videos' : videos
    }
    return render(request,'search/index.html' , context)




    
