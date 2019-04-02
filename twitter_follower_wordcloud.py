# -*- coding: utf-8 -*-
"""
This script generates a wordcloud using words extracted from twitter
bios. Bios are taken from followers of a target account, thus providing a 
crude means of qualitatively assessing the followers of the target account.

Users must gain Developer Access for their twitter account in order to
access the twitter API via the tweepy python library. See link below 
for details on how to do this.

Also, please excuse any non-pythonic structure. I'm a complete n00b at this.

Cheers,
Osty.

https://developer.twitter.com/en/apply-for-access.html
"""

# import common libraries
import os, time
import matplotlib.pyplot as plt

# import uncommon libraries, you may need to install these
import tweepy
from wordcloud import WordCloud
from tweepy import OAuthHandler

# input twitter developer details for API access requirements
consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXX'                              # 25 character string
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # 50 character string
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'     # 50 character string
access_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # 45 character string
auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

# define target account and number of most recent tweets to look at
account = 'your_twitter_handle' # twitter handle here (eg: 'nature' for @nature)
max_followers = 100             # max number of followers to extract bios for
# path to output directory
outdir = r"D:\your_directory_of_choice\twitter_bio_wordclouds"

# set api variable using authority details
api = tweepy.API(auth, wait_on_rate_limit=True)

# get list of follower IDs for user account
user_acc_followers = tweepy.Cursor(api.followers_ids,screen_name=account)
follower_ids = [x for x in user_acc_followers.pages()]
follower_ids = [x for i in follower_ids for x in i]

# get twitter bio info for followers
text = []
for idx,i in enumerate(follower_ids):
    print 'Working on follower', idx + 1
    user = api.get_user(id=i)
    bio = (user.description).encode("utf-8")
    for j in bio.strip().split():
        text.append(j)
    if idx + 1 == max_followers:
        print 'Maximum number of followers reached'
        break

# do some basic filtering to clean up nonsense
# make all items lower case
text = [str.lower(x) for x in text]

# remove any strings containing numbers
text = [x for x in text if not any(c.isdigit() for c in x)] 

# remove strings containing various symbols
filter_items = ['/',':','|','\\']
for i in filter_items:
    text = [x for x in text if not any(c==i for c in x)]    

# remove empty strings 
text = filter(None,text) 

# print some details to console/terminal
print '------------'
print 'Extracting bios for followers of @%s' %(account)
print 'Total number of followers:', len(follower_ids)
print 'Total number of followers used:', max_followers
print 'Total number of words:', len(text)
print '------------'

# generate wordcloud
wordcloud = WordCloud(background_color="white",
                      colormap='viridis',
                      height=600,
                      width=1068,
                      max_words=100)

wordcloud.generate(" ".join(text))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# make output file name for wordcloud image using date and time
t = time.localtime()[0:6]
outname = 'wordcld_%s_%s%s%s-%s%s%s.png' %(account,t[0],t[1],t[2],t[3],t[4],t[5],)
outfn = os.path.join(outdir,outname)

# save wordcloud to output directory
wordcloud.to_file(outfn)

# print some more details to console/terminal
print 'Wordcloud saved to:  ', outname
print 'File naming format:  ', 'wordcld_*account*_*datecode*_*timecode*'
print '------------ JOB DONE ------------'

# open the wordcloud
plt.show()
