#!/usr/bin/python
# encoding : utf-8
import yt_dlp
import re
from flup.server.fcgi import WSGIServer

def load_video(video_url):
    response_arr = ''
    ydl_opts = {}
    ydl_opts['username'] = 'oauth2'
    ydl_opts['password'] = ''
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        date_info = ydl.extract_info(video_url, download=False)
        info = ydl.sanitize_info(date_info)
        for video_format in info['formats']:
            response_arr = response_arr + str(video_format['format']) + ':\n' + str(video_format['url']) + '\n\n\n'
    return [response_arr]

def get_video_url(param_str):
    param_str = str(param_str)
    print(param_str)
    if re.match(r'^https?:/{2}\w.+$', param_str):
        return param_str, True
    else:
        return 'This looks invalid.\n', False

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    url, result = get_video_url(environ["QUERY_STRING"])
    if not result :
        return [url]
    return load_video(url)


if __name__  == '__main__':
    print("start...")
    WSGIServer(myapp,bindAddress=('127.0.0.1',8899)).run()
    print("ending...")