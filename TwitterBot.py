import tweepy
import json
from datetime import datetime
import time
import os
import requests

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
draft = False
season_started = False
rosters = True

# Handles tweets
# ------------------------------------------------------------------------------------------------ #☺
if(datetime.today().strftime('%A') == 'Monday' and season_started == True): #Tweets made on monday

    with open(data_path + "/standings/standings.json") as S: # Loads Current Standings Information
        Standings = json.load(S)
    
    current_week = Standings['current_week'] # Saves current week

    tweet = "WEEK " + current_week + " STANDINGS\n\n" # Starts Standings Tweet
    for i in range(0, 6): # Adds top 6 teams
        tweet += str(i+1) + " - " + Standings['standings'][i]['Name']
        tweet += " (" + str(Standings['standings'][i]['Wins']) + " - " + str(Standings['standings'][i]['Losses']) + ") \n"

    original_tweet = api.update_status(tweet) #Tweets top 6 teams
    
    tweet = "" # Starts an empty tweet
    for i in range(6, 12): # Adds bottom 6 teams
        tweet += str(i+1) + " - " + Standings['standings'][i]['Name']
        tweet += " (" + str(Standings['standings'][i]['Wins']) + " - " + str(Standings['standings'][i]['Losses']) + ") \n"

    api.update_status(status=tweet, in_reply_to_status_id = original_tweet.id) #Adds a reply to the original tweet with bottom 6 teams

    print("Tweeted Standings")
    time.sleep(30)

    with open(data_path + "/standings/"+ datetime.now().strftime("%b") + ".json") as S: # Loads Monthly Standings Information
        Monthly = json.load(S)
    
    current_month = datetime.now().strftime("%B").upper() # Current month name
    
    tweet = current_month + " STANDINGS\n\n" # Starts Standings Tweet
    for i in range(0, 6): # Adds top 6 teams
        tweet += str(i+1) + " - " + Monthly[i]['Name']
        tweet += " (" + str(Monthly[i]['Wins']) + " - " + str(Monthly[i]['Losses']) + ") \n"

    original_tweet = api.update_status(tweet) #Tweets top 6 teams
        
    tweet = "" # Starts an empty tweet
    for i in range(6, 12): # Adds bottom 6 teams
        tweet += str(i+1) + " - " + Monthly[i]['Name']
        tweet += " (" + str(Monthly[i]['Wins']) + " - " + str(Monthly[i]['Losses']) + ") \n"
        
    api.update_status(status=tweet, in_reply_to_status_id = original_tweet.id) #Adds a reply to the original tweet with bottom 6 teams

    print("Tweeted Monthly Standings")
    time.sleep(30)

    with open(data_path + "/freeagents/FreeAgents.json") as FA: # Loads Free Agents Information
        FreeAgents = json.load(FA)
    
    tweet = "WEEK " + current_week + " TOP FREE AGENTS!!\n\n" # Starts Free Agents Tweet

    for i in range(5): # Adds top 5 Free agents to the tweet
        tweet += str(i+1) + " - " + FreeAgents[i]['Name']
        tweet += " (" + FreeAgents[i]['Positions'] + ") - " + FreeAgents[i]['Team'] + "\n"
    api.update_status(tweet)
    print("Tweeted top free agents")
    time.sleep(30)

# Everyday tweets

with open(data_path + "/transactions/newTransactions.json") as T: # Loads Transactions Information
    Transactions = json.load(T)

if(len(Transactions) > 0): # If there are new transactions
    tweet = "LATEST TRANSACTIONS:\n\n"
    for i in range(len(Transactions)):
        tweet += Transactions[i]['type']
    api.update_status(tweet)
    print("Tweeted Transactions")


if(draft):
    with open("./MockDraft.json") as M: # Loads Transactions Information
        MockDraft = json.load(M)

    tweet = "MOCK DRAFT 1.1 \n\n"
    original_tweet = api.update_status(tweet)

    for i in range(13): #Number of rounds
        tweet = "Round #" + str(i+1) + '\n'
        for j in range(12*i, 12*i + 12): # gets entire round, 12 teams
            tweet += '#' + str(j+1) + ' - ' + MockDraft[j]['Name'] + "\n"
        original_tweet = api.update_status(status=tweet, in_reply_to_status_id = original_tweet.id)
        time.sleep(30)

if(rosters):
    with open(data_path + "/rosters/Rosters.json") as R: # Loads Rosters Information
        rosters = json.load(R)
    
    tweet = "OFFICIAL ROSTERS FOR THE 2021-2022 SEASON"
    original_tweet = api.update_status(tweet)

    for i in range(len(rosters)):
        filename = 'temp.jpg' #Defines a temp file
        tweet = rosters[i]['Name'] + " (" + rosters[i]['Nickname'] + ")\n\n" #Starts tweet
        for j in range(len(rosters[i]['players'])): # Adds players to tweet
            tweet += rosters[i]['players'][j]['Name'] + "\n"
        tweet += "\n"
        
        request = requests.get(rosters[i]['Team logo'], stream=True) #gets team logo
        
        if request.status_code == 200: #If was able to get logo
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            media = api.media_upload(filename).media_id
            original_tweet = api.update_status(tweet, media_ids = [media], in_reply_to_status_id = original_tweet.id) #tweets with logo
            os.remove(filename)
        else:
            print("Unable to download image")
        
        time.sleep(30)
    print('tweeted Rosters')
