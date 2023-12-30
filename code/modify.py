import json

filteredVideos = categories = json.load(open('out.json'))

categories = json.load(open('US_category_id.json'))['items']

for i in range(len(filteredVideos)):
  #filteredVideos[i].categoryId
  for c in categories:
    if(c['id'] == filteredVideos[i]['categoryId']):
      filteredVideos[i]['category'] = c['snippet']['title']
      break


with open('out_with_cat.json', 'w') as f:
  json.dump(filteredVideos, f)

print('success')
