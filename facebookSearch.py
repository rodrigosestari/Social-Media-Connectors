import os

# https://developers.facebook.com/tools/explorer/?method=GET&path=me%3Ffields%3Did%2Cname&version=v3.2
import facebook

token = str(os.environ.get('facebook_token',''))
graph = facebook.GraphAPI(access_token=token, version=3.1)

events = graph.request('/search?q=aquafresh&type=post&limit=10000')
places = graph.search(type='place',
                      center='37.4845306,-122.1498183',
                      fields='name,location')

# Each given id maps to an object the contains the requested fields.
for place in places['data']:
    print('%s %s' % (place['name'].encode(), place['location'].get('zip')))
