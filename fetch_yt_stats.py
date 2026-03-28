import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

try:
    with open('/root/.openclaw/workspace/youtube_token.json') as f:
        t = json.load(f)

    creds = Credentials(token=t['token'], refresh_token=t['refresh_token'],
        token_uri=t['token_uri'], client_id=t['client_id'],
        client_secret=t['client_secret'], scopes=t['scopes'])

    if creds.expired:
        creds.refresh(Request())
        t['token'] = creds.token
        with open('/root/.openclaw/workspace/youtube_token.json','w') as f: json.dump(t,f)

    yt = build('youtube','v3',credentials=creds)
    ch = yt.channels().list(part='statistics,snippet', mine=True).execute()
    stats = ch['items'][0]['statistics']

    search_res = yt.search().list(part='snippet', forMine=True, type='video', maxResults=5).execute()
    video_list = []
    for v in search_res.get('items', []):
        vid_id = v['id']['videoId']
        vs = yt.videos().list(part='statistics', id=vid_id).execute()
        vstats = vs['items'][0]['statistics'] if vs['items'] else {}
        video_list.append({
            'title': v['snippet']['title'][:45],
            'views': vstats.get('viewCount','0'),
            'likes': vstats.get('likeCount','0'),
            'comments': vstats.get('commentCount','0')
        })

    data = {
        'subscribers': stats.get('subscriberCount','0'),
        'totalViews': stats.get('viewCount','0'),
        'videoCount': stats.get('videoCount','0'),
        'videos': video_list,
        'updated': __import__('datetime').datetime.utcnow().strftime('%H:%M UTC')
    }
except Exception as e:
    data = {'subscribers': 'N/A', 'totalViews': 'N/A', 'videoCount': 'N/A', 'videos': [], 'error': str(e)}

with open('/root/.openclaw/workspace/yt_stats.json', 'w') as f:
    json.dump(data, f)

print("Done:", data['videoCount'], "videos")
