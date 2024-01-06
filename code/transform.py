import pandas as pd
from util import parseCsvToArray

def getViewsLikesComments(channelId = None):
  # Primary data
  videos = parseCsvToArray('US_youtube_trending_data.csv')

  # Sum views, likes and dislikes by month and year
  views = dict()
  likes = dict()
  comments = dict()

  # Keep track of video IDs which duplicate on trends and keep only
  # the latest (greatest amount of views).
  duplicates = dict()

  for i in range(len(videos)):

    if channelId != None:
      if channelId != videos[i]['channelId']:
        continue

    date = videos[i]['publishedAt']
    simplerDate = date[0:7] + '-01'

    videoId = videos[i]['video_id']

    # Check if video is a duplicate or not.
    if videoId not in duplicates:
      duplicates[videoId] = videos[i]
    # Check if this trending entry is newer than the duplicate one.  
    elif videos[i]['view_count'] > duplicates[videoId]['view_count']:
      # Subtract the views from the existing duplicate in order to add the new value.  
      views[simplerDate] -= int(videos[i]['view_count'])
      likes[simplerDate] -= int(videos[i]['likes'])
      comments[simplerDate] -= int(videos[i]['comment_count'])
      duplicates[videoId] = videos[i]

    if simplerDate not in views:
      views[simplerDate] = int(videos[i]['view_count'])
      likes[simplerDate] = int(videos[i]['likes'])
      comments[simplerDate] = int(videos[i]['comment_count'])
    else:
      views[simplerDate] += int(videos[i]['view_count'])
      likes[simplerDate] += int(videos[i]['likes'])
      comments[simplerDate] += int(videos[i]['comment_count'])

  return  {'views': views, 'likes': likes, 'comments': comments}

data = getViewsLikesComments()

df = pd.DataFrame.from_dict(data['views'], orient="index")
df.to_csv('viewsPerYear.csv')

df = pd.DataFrame.from_dict(data['likes'], orient="index")
df.to_csv('likesPerYear.csv')

df = pd.DataFrame.from_dict(data['comments'], orient="index")
df.to_csv('commentsPerYear.csv')

dataMrBeast = getViewsLikesComments('UCX6OQ3DkcsbYNE6H8uQQuVA')

df = pd.DataFrame.from_dict(dataMrBeast['views'], orient="index")
df.to_csv('viewsPerYearBeast.csv')

df = pd.DataFrame.from_dict(dataMrBeast['likes'], orient="index")
df.to_csv('likesPerYearBeast.csv')

df = pd.DataFrame.from_dict(dataMrBeast['comments'], orient="index")
df.to_csv('commentsPerYearBeast.csv')
