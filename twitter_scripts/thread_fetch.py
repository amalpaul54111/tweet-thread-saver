import requests
import json
from twitter_scripts import secrets
from twitter_scripts import urls
from twitter_scripts import Write
from twitter_scripts import fetch_mention
#import secrets
#import urls
#import Write
#import fetch_mention

mId='threadsaverbfh'

def auth():
    return secrets.bearer_key


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

    
    userData={
            'thread_author':thread_author['data']['name'],
            'thread_author_username':'@'+thread_author['data']['username'],
            'thread_tweets':tweet,
            'conversation_id': conversation_id,
            }
    # print(userData)
    return userData


def get_threads(twitterUserName):
    ids = fetch_mention.last_mentioned_ids(twitterUserName)
    userData=get_tweets(ids)
    return userData

def create_ids(ids):
    tweet_fields = "tweet.fields=author_id,conversation_id,text,id,created_at,attachments,in_reply_to_user_id"
    idString=''

    for i in ids:
        idString+=f"{i},"
    idFiltered= idString[:-1]
    print(idFiltered)
    url = "https://api.twitter.com/2/tweets?ids={}&tweet.fields=author_id,text,id".format(idFiltered)
    return url


def get_tweets(conversation_ids):
    bearer_token = auth()
    headers = create_headers(bearer_token)


    url = create_ids(conversation_ids)
    tweets = connect_to_endpoint(url, headers)
    for i in tweets['data']:
        author_id = i['author_id']
        url = urls.create_username(author_id)
        thread_author = connect_to_endpoint(url,headers)
        i['thread_author']=thread_author['data']['name']
        i['thread_author_username']=thread_author['data']['username']
        i['text']+= getaddOnTweets(i['id'],i['author_id'])
        i['thread_tweets']=[i['text']]
        i['conversation_id']= i['id']

    # Write.write_author_only(thread_convo, thread_original_tweet, thread_author)
    return tweets['data']



#pass twitterUserName in main
def main(twitterUserName):
    data = get_threads(twitterUserName)
    return data

def myPrint(tweets):
    file=open('./output/tweets.txt','w')
    for tweet in tweets:
        file.write(f"{tweet['thread_author']} -- {tweet['thread_author_username']} \n  {tweet['text']}\n\n \n")


def addByUrl(url):
    urlSplit=url.split('status/') 
    return get_tweets([urlSplit[1]])

def getaddOnTweets(convId, authorId):
    url = urls.create_convo(convId)
    bearer_token = auth()
    headers = create_headers(bearer_token)
    thread_convo = connect_to_endpoint(url, headers)
    author_convo =''
    if 'data' in thread_convo.keys():
        for reply in thread_convo['data']:
            if reply['in_reply_to_user_id'] == authorId and reply['author_id']==authorId:
                author_convo+=f" {reply['text']}"
    return author_convo


if __name__ == "__main__":
    main("thejaskiranps")

