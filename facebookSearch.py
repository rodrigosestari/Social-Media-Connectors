import os

import facebook
import requests

token = str(os.environ.get('facebook_token', ''))
graph = facebook.GraphAPI(access_token=token, version=2.7)
pagesdata = requests.get("https://graph.facebook.com/me/accounts?access_token = " + token)
page_id = "161674417186975"
posts_on_page = requests.get("https://graph.facebook.com/" + page_id + "/feed?access_token = " + token)
posts_data = (posts_on_page.json())
# print posts_data
for x in posts_data['data']:
    post_id = x['id']
reactions_on_post = requests.get("https://graph.facebook.com/" + post_id + "/reactions?access_token = " + token)
reactions_data = reactions_on_post.json()
print(reactions_data)

places = graph.search(type='place',
                      center='37.4845306,-122.1498183',
                      fields='name,location')

# Each given id maps to an object the contains the requested fields.
for place in places['data']:
    print('%s %s' % (place['name'].encode(), place['location'].get('zip')))
