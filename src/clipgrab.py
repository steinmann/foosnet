import requests
import os


def bash(command):
    # execute bash command using linux subsystem (ubuntu)
    os.system('bash -c \'{}\''.format(command))


def get_video_ids(channel_id, api_key):
    # return list of all video ids from channel
    auth = {
            'api_key': api_key,
            'channel_id': channel_id,
            'base_url': 'https://www.googleapis.com/youtube/v3/'
    }

    channel_url_template = '{base_url}channels?part=contentDetails&id={channel_id}&key={api_key}'
    channel_details = requests.get(channel_url_template.format(**auth)).json()
    auth['playlist_id'] = channel_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']


    playlist_url = '{base_url}playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={api_key}'.format(**auth)
    playlist_details = requests.get(playlist_url).json()
    playlist_items = playlist_details['items']

    while playlist_details.get('nextPageToken'):
        playlist_details = requests.get('{}&pageToken={}'.format(playlist_url, playlist_details['nextPageToken'])).json()
        playlist_items.extend(playlist_details['items'])

    return [item['contentDetails']['videoId'] for item in playlist_items]


def get_clip(video_id, offset):
    config = {
             'v_id': video_id,
             'offset': offset,
             'base_url': 'https://www.youtube.com/watch?v='
    }
    template = 'ffmpeg -v 0 -ss {offset} -i $(youtube-dl -f 22 -g \'{base_url}{v_id}\') -q 0 -vframes 1 -y {v_id}_{offset}.jpg'
    bash(template.format(**config))


def process():
    my_api_key = 'AIzaSyAAA2PwqB0PYBqmcS4mIAZ5Y3RpAi3sZlk'
    p4p4_channel_id = 'UCRtugJkSFMQgp_22sqkFC4g'
    video_ids = get_video_ids(p4p4_channel_id, my_api_key)
    print(video_ids)
    count = 0
    offsets = [60, 120, 180, 240, 300, 360, 420, 480, 540, 600]
    for offset in offsets:
        for video_id in video_ids:
            count += 1
            print('{} Retrieving jpg for {}'.format(count, video_id))
            get_clip(video_id, offset)

process()
