#https://towardsdatascience.com/tutorial-using-youtubes-annoying-data-api-in-python-part-1-9618beb0e7ea
#https://developers.google.com/youtube/v3/code_samples/python_appengine#search_by_keyword
#https://developers.google.com/youtube/v3/code_samples/python
from pytube import YouTube
YouTube('https://youtu.be/9bZkp7q19f0').streams.first().download()
yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()