import csv
import json
import pandas as pd
from datetime import datetime
import os

# Transfrom a csv file to array
def parseCsvToArray(filename):
  reader = csv.reader(
      open(filename, 'r', encoding='utf-8'))
  data = []
  headers = next(reader)
  nextLine = next(reader)
  while nextLine != None:
    obj = {}
    for i in range(len(headers)):
      obj[headers[i]] = nextLine[i]
    data.append(obj)
    try:
      nextLine = next(reader)
    except StopIteration:
      break
    except Exception:
      continue

  return data

# Primary data
videos = parseCsvToArray('US_youtube_trending_data.csv')

# Limit data to 4 years
years = []
for i in range(len(videos)):
  year = videos[i]['publishedAt']
  sub = year[0:4]
  if sub not in years:
    years.append(sub)

channels = parseCsvToArray('most_subscribed_youtube_channels.csv')

# Filter primary data for only the most subscribed channels
filteredVideos = []
for i in range(len(channels)):
  channelVideos = list(filter(lambda c: c['channelTitle'] == channels[i]['Youtuber'], videos))
  filteredVideos = filteredVideos + channelVideos

categories = json.load(open('US_category_id.json'))['items']

# Add category title 
for i in range(len(filteredVideos)):
  # Convert dates for use on orange 
  publishedString = datetime.strptime(filteredVideos[i]['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
  filteredVideos[i]['publishedAt'] = str(publishedString.strftime("%Y-%m-%d %H:%M:%S"))

  trendingString = datetime.strptime(filteredVideos[i]['trending_date'], "%Y-%m-%dT%H:%M:%SZ")
  filteredVideos[i]['trending_date'] = str(trendingString.strftime("%Y-%m-%d %H:%M:%S"))

  for c in categories:
    if c['id'] == filteredVideos[i]['categoryId']:
      filteredVideos[i]['category'] = c['snippet']['title']
      break

# Create CSV
os.remove('out.csv')

jsonStr = json.dumps(filteredVideos)
df = pd.read_json(jsonStr)
df.to_csv('out.csv')
