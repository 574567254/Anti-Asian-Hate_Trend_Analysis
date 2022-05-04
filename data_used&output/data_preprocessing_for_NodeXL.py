# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 21:42:35 2022

@author: xintong
"""

import pandas as pd

tweet = pd.read_csv('tweets_NYTS_asianwomandies.csv')

tweet_text  = tweet.Text.values
tweet_text = tweet_text.tolist()
user = tweet.Username.values
user = user.tolist()

#detect non-english languages
df = pd.DataFrame(list(zip(tweet_text, user)),columns = ["tweet",'user'])

from langdetect import detect
language = []
for i in range(len(df.tweet)):
    lan = detect(df.tweet.iloc[i])
    language.append(lan)

non_en = []
for i in range(len(language)):
    if language[i] != 'en':
        non_en.append(i)
        
df = df.drop(non_en) ## drop non-english tweet

en_text = df.tweet.values

import re
non_tweet_users = []
for t in en_text:
    
    non_tweet_users.append(re.findall(r'[@]\S*', t))

tweet_users = df.user.values

for i in range(len(non_tweet_users)):
    if len(non_tweet_users[i]) == 0:
        continue
    else:
        for j in range(len(non_tweet_users[i])):
            char = list(non_tweet_users[i][j])
            char.remove('@')
            name = ''.join(char)
            non_tweet_users[i][j] = name   

#detect tweet type
typ = []
for i in non_tweet_users:
    if len(i) == 0:
        typ.append('t')
    else:
        typ.append('nt')
        
#final output
output = pd.DataFrame(columns = ['column1','column2','type'])
for i in range(len(typ)):
    if typ[i] == 't':
        output = output.append(pd.Series([tweet_users[i],tweet_users[i],typ[i]], index=['column1','column2','type']), ignore_index=True)
    if typ[i] != 't':
        for j in range(len(non_tweet_users[i])):
            output = output.append(pd.Series([non_tweet_users[i][j],tweet_users[i],typ[i]], index=['column1','column2','type']), ignore_index=True)
            
            
ind = []
for i in range(len(output.column1)):
    if output.column1[i] == '':
        ind.append(i)
        
output = output.drop(ind)
output.to_csv('data_for_NodeXL.csv', index=True)