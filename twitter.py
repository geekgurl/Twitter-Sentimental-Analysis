import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight') 


from google.colab import files
uploaded=files.upload


log=pd.read_csv('login.csv')


consumerkey=log['key'][0]
consumersecret=log['key'][1]
accesstoken=log['key'][2]
accesstokensecret=log['key'][3]


authenticate=tweepy.OAuthHandler(consumerkey,consumersecret)


authenticate.set_access_token(accesstoken,accesstokensecret)

api=tweepy.API(authenticate,wait_on_rate_limit=True)


#Extract 100 tweets from twitter user
posts=api.user_timeline(screen_name="BillGates",count=100,lang="en",tweet_node="extended")

#print the last 5 tweets from the account
print("Show the 5 recent tweets: \n")
i=1 
for tweet in posts[0:5]:
     print(str(i) + ')' +tweet.full_text+'\n')
     i=i+1

#create a data frame with a cloumn called tweets
df=pd.DataFrame([tweet.full_text for tweet in posts],cloumns=['tweets'])

#show the first 5 rows of data
df.head()

#clean text
def cleantxt(text):
    text=re.sub('@[A-Za-z0-9]+', '',text)#Removed @mentions
    text=re.sub(r'#','',text)
    text=re.sub(r'RT[\s]+','',text)
    text=re.sub(r'https?:\/\/\S+','',text)

    return text


df['tweets']=dcf['tweets'].apply(cleantxt)


#create a function to get the subjectivity
def getsubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

#create a function to get the polarity
def getpolarity(text):
    return TextBlob(text).sentient.polarity


#create two new cloumns
df['subjectivity']=df['tweets'].apply(getsubjectivity)
df['polarity']=df['tweets'].apply(getpolarity)

#plot the word cloud
allwords=''.join([twts for twts in df['tweets']])
wordCloud=WordCloud(width=500,height=300,random_state=21,max_font_size=119).generate(allwords)

plt.imshow(wordcloud,interpolation="bilinear")
plt.axis('off')
plt.show()

#create a function to compute a -ve,neutral and +ve analysis
def getAnalysis(score):
    if score <0:
        return 'Negative'
    elif score ==0:
        return 'Neutral'
    else:
        return 'Positive'

df['Analysis']=df['polarity'].apply(getAnalysis)


#print all of the positive tweets
j=1
sortedDF=df.sort_values(by=['polarity'])
for i in range(0,sortedDF.shape[0]):
    if(sortedDF['Analysis'][i]=='Positive'):
        print(str(j)+')'+sortedDF['tweets'][i])
        print()
        j=j+1

#print -ve tweets
j=1
sortedDF=df.sort_values(by=['polarity'],ascending='False')
for i in range(0,sortedDF.shape[0]):
    if(sortedDF['Analysis'][i]=='Negative'):
        print(str(j)+')'+sortedDF['tweets'][i])
        print()
        j=j+1

#plot the polarity and subjectivity
plt.figure(figsize=(8,6))
for ni in range(0,df.shape[0]):
    plt.scatter(df['polarity'][i],df['subjectivity'][i],color='blue')

plt.title('Sentiment Analysis')
plt.xlabel('polarity')
plt.ylabel('subjectivity')
plt.show()

#get the percentage of +ve tweets
ptweets=df[df.Analysis=='Positive']
ptweets=ptweets['tweets']

round((ptweets.shape[0]/df.shape[0])*100,1)

#get the percentage of -ve tweets
ptweets=df[df.Analysis=='Negative']
ptweets=ptweets['tweets']

round((ptweets.shape[0]/df.shape[0])*100,1)

#show the value counts
df['Analysis'].value_counts
#plot and visulaize the counts()
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()







