import tweepy
import json
import datetime

# Loads credentials from auth file
with open('./auth/botauth.json') as json_file:
    auths = json.load(json_file)
consumer_key = auths['key']
consumer_secret = auths['secret']
access_key = auths['token']
access_secret = auths['token_secret']
json_file.close()

# Handles authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

data_path = './fantasytracker/src/Components/Data' #Path to data folders

# Handles tweets

with open(data_path + "/freeagents/FreeAgents.json") as FA: # Loads Free Agents Information
    FreeAgents = json.load(FA)

with open(data_path + "/standings/Standings.json") as S: # Loads Current Standings Information
    Standings = json.load(S)

current_week = Standings['current_week']
tweet = "WEEK " + current_week + " TOP FREE AGENTS!! \n"

for i in range(5):
    tweet += str(i+1) + " - " + FreeAgents[i]['Name'] + " (" + FreeAgents[i]['Positions'] + ") - " + FreeAgents[i]['Team'] + "\n"

