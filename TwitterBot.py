import tweepy
import json
from datetime import datetime
import time
import os
import requests
import random

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
rosters = False
season_started = True
more_than_a_week = True

# Handles tweets
# ------------------------------------------------------------------------------------------------ #☺
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

if(datetime.today().strftime('%A') == 'Monday' and season_started == True): #Tweets made on monday+

    if(more_than_a_week == True):
        with open("PrevSchedule.json") as S: # Loads Schedule information
            PrevSchedule = json.load(S)

        tweet = "WEEK " + str(PrevSchedule['Week']) + " MATCHUP RESULTS" # Starts thread
        original_tweet = api.update_status(tweet) # Posts original tweet

        for i in range(6): #Goes through all matchups
            if PrevSchedule['Matches'][i]['Team1 Points'] > PrevSchedule['Matches'][i]['Team2 Points']:
                winner = PrevSchedule['Matches'][i]['Team1']
                winner_points = PrevSchedule['Matches'][i]['Team1 Points']
                loser = PrevSchedule['Matches'][i]['Team2']
                loser_points = PrevSchedule['Matches'][i]['Team2 Points']
            else:
                winner = PrevSchedule['Matches'][i]['Team2']
                winner_points = PrevSchedule['Matches'][i]['Team2 Points']
                loser = PrevSchedule['Matches'][i]['Team1']
                loser_points = PrevSchedule['Matches'][i]['Team1 Points']

            rand = random.randint(1,3) # Decides what message will be tweeted

            tweet = "The " + winner
            if(winner_points - loser_points >= 200):
                if(rand == 1):
                    tweet += " blow out the "
                if(rand == 2):
                    tweet += " destroy the  "
                if(rand == 3):
                    tweet += " breeze through the "
            elif(winner_points - loser_points <= 20):
                if(rand == 1 or rand == 3):
                    tweet += " survive against the "
                if(rand == 2):
                    tweet += " barely defeat the "
            else:
                if(rand == 1):
                    tweet += " beat the "
                if(rand == 2):
                    tweet += " defeat the "
                if(rand == 3):
                    tweet += " prevail against the "

            tweet += loser + " in a " + str(winner_points) + " - " + str(loser_points)
            if(winner_points - loser_points <= 20):
                tweet += " nail bitter"
            tweet += " win!"
            if(winner_points - loser_points <= 10):
                tweet += " A true fantasy classic!"
            if PrevSchedule['Playoffs'] == "1":
                tweet += "\nThe " + loser + " has been eliminated!\n"
            original_tweet = api.update_status(status=tweet, in_reply_to_status_id = original_tweet.id) #Adds a reply to the thread with the next matchup
            time.sleep(10)
        print("tweeted results\n")


    with open(data_path + "/standings/standings.json") as S: # Loads Current Standings Information
        Standings = json.load(S)
    
    current_week = Standings['current_week'] # Saves current week

    tweet = "WEEK " + str(current_week) + " STANDINGS\n\n" # Starts Standings Tweet
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


    with open("Schedule.json") as S: # Loads Schedule information
        Schedule = json.load(S)
    
    if Schedule['Playoffs'] == "1":
        tweet = "THIS WEEK´S PLAYOFF MATCHES"# Starts thread
    else:
        tweet = "WEEK " + str(current_week) + " MATCHUPS" # Starts thread
    
    original_tweet = api.update_status(tweet) # Posts original tweet

    for i in range(6): #Goes through all matchups
        tweet = "The " + Schedule['Matches'][i]['Team1'] + " (" + str(Schedule['Matches'][i]['Team1 Projected']) + " projected points, " + str(Schedule['Matches'][i]['Team1 Matches']) + " projected matches) "
        rand = random.randint(1,3) # Decides what message will be tweeted
        if(rand == 1):
            tweet += "will face "
        if(rand == 2):
            tweet += "goes against "
        if(rand == 3):
            tweet += "faces off "
        tweet += "the " + Schedule['Matches'][i]['Team2'] + " (" + str(Schedule['Matches'][i]['Team2 Projected']) + " projected points, " + str(Schedule['Matches'][i]['Team2 Matches']) + " projected matches) "
        original_tweet = api.update_status(status=tweet, in_reply_to_status_id = original_tweet.id) #Adds a reply to the thread with the next matchup
        time.sleep(10)
    print("tweeted schedule\n")

    
    with open(data_path + "/freeagents/FreeAgents.json") as FA: # Loads Free Agents Information
        FreeAgents = json.load(FA)
    
    tweet = "WEEK " + str(current_week) + " TOP FREE AGENTS!!\n\n" # Starts Free Agents Tweet

    for i in range(5): # Adds top 5 Free agents to the tweet
        tweet += str(i+1) + " - " + FreeAgents[i]['Name']
        tweet += " (" + FreeAgents[i]['Positions'] + ") - " + FreeAgents[i]['Team'] + "\n"
    api.update_status(tweet)
    print("Tweeted top free agents")
    time.sleep(30)


# Everyday tweets

with open(data_path + "/transactions/newTransactions.json") as T: # Loads Transactions Information
    Transactions = json.load(T)

Transactions.reverse() # Reverse

for i in range(len(Transactions)): # Goes through transactions
    if(Transactions[i]['Type'] == 'add'): # If its an add
        rand = random.randint(0,3) # Decides what message will be tweeted
        if(rand == 0):
            tweet = "Free Agent " + Transactions[i]['Players'][0]['Name'] + " has agreed to a 1 year minimum contract with the "
            tweet += Transactions[i]['Players'][0]['Destination'] + ", sources tell NPSE"
        if(rand == 1):
            tweet = "Free Agent " + Transactions[i]['Players'][0]['Name'] + " is joining the "
            tweet += Transactions[i]['Players'][0]['Destination'] + " on a 1 year minimum contract, sources tell NPSE"
        if(rand == 2):
            tweet = "The " + Transactions[i]['Players'][0]['Destination'] + " have reached an agreement with Free Agent "
            tweet += Transactions[i]['Players'][0]['Name'] + " on a 1 year minimum contract, sources tell NPSE"
        if(rand == 3):
            tweet = "Free Agent " + Transactions[i]['Players'][0]['Name'] + " is headed to the "
            tweet += Transactions[i]['Players'][0]['Destination'] + " on a 1 year minimum contract, sources tell NPSE"
            
    if(Transactions[i]['Type'] == "add/drop"):  # If its an add/drop
        rand = random.randint(0,2) # Decides what message will be tweeted
        if(rand == 0):
            tweet = "The " + Transactions[i]['Players'][0]['Destination'] + " and " + Transactions[i]['Players'][1]['Name']
            tweet += " have agreed on a buyout. After clearing waivers, they will look to add " + Transactions[i]['Players'][0]['Name'] 
            tweet += " on a 1 year minimum contract, sources tell NPSE"
        if(rand == 1):
            tweet = Transactions[i]['Players'][1]['Name'] + " has agreed on a contract buyout with the " +  Transactions[i]['Players'][0]['Destination']
            tweet += ". Upon clearing waivers, they plan to sign " + Transactions[i]['Players'][0]['Name'] 
            tweet += " on a 1 year minimum contract, sources tell NPSE"
        if(rand == 2):
            tweet = "The " + Transactions[i]['Players'][0]['Destination'] + " has agreed to a 1 year minimum contract with "
            tweet += Transactions[i]['Players'][0]['Name'] + ", league sources tell NPSE. In order to open a roster space, they are parting ways with "
            tweet += Transactions[i]['Players'][1]['Name'] 

    if(Transactions[i]['Type'] == "drop"): # If its a drop
        rand = random.randint(0,3) # Decides what message will be tweeted
        if(rand == 0):
            tweet = "The " + Transactions[i]['Players'][0]['Source'] + " and " + Transactions[i]['Players'][0]['Name']
            tweet += " have agreed on a contract buyout, sources tell NPSE"
        if(rand == 1):
            tweet = Transactions[i]['Players'][0]['Name'] + " has agreed on a contract buyout with the " +  Transactions[i]['Players'][0]['Source'] + ", sources tell NPSE"
        if(rand == 2):
            tweet = "The " + Transactions[i]['Players'][0]['Source'] + " and " + Transactions[i]['Players'][0]['Name']+ " are parting ways, sources tell NPSE"
        if(rand == 3):
            tweet = "The " + Transactions[i]['Players'][0]['Source'] + " are parting ways with " + Transactions[i]['Players'][0]['Name'] + ", sources tell NPSE"
    
    if(Transactions[i]['Type'] == "trade"): # If its a trade
        tweet = "The " + Transactions[i]['Players'][0]['Source'] + " are trading " + Transactions[i]['Players'][0]['Name'] #Starts the tweet

        for j in range(1, len(Transactions[i]['Players'])): # Finds all players that will be traded from first team
            if Transactions[i]['Players'][j]['Source'] == Transactions[i]['Players'][0]['Source']:
                tweet += ", " + Transactions[i]['Players'][j]['Name']
            else:
                tweet += " to the " + Transactions[i]['Players'][j]['Source'] + " for " +  Transactions[i]['Players'][j]['Name']
                break

        for k in range(j+1, len(Transactions[i]['Players'])): # Finds all players that will be traded from second team
            tweet += ", " + Transactions[i]['Players'][k]['Name']
        tweet += "."
    api.update_status(tweet)
    time.sleep(10)
print("tweeted transactions\n")


