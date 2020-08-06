# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 19:10:21 2020

@author: Tanya Shourya
"""
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import re
#from gensim.summarization import keywords

print ('Wordcloud is installed and imported!')
db = pd.read_csv('twitter.csv')
tweet_list = db['tweet_list']
tweet_str = ''.join(tweet_list)
#cleaning data
text = tweet_str.lower()
text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
tweet_mask = np.array(Image.open('tweet_mask.png'))
stopwords = set(STOPWORDS)
stopwords.add('co')
stopwords.add('https')
stopwords.add('RT')
tweet_wc = WordCloud(
    background_color='white',
    max_words=200,
    stopwords=stopwords,
    collocations=False,
    mask = tweet_mask,
)
tweet_wc.generate(tweet_str)

fig = plt.figure()
fig.set_figwidth(24) # set width
fig.set_figheight(18) # set height

# display the cloud
plt.imshow(tweet_mask, cmap=plt.cm.gray,interpolation='bilinear')
plt.imshow(tweet_wc, interpolation='bilinear')
plt.axis('off')
plt.show()