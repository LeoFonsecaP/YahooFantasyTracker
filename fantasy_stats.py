from yahoo_oauth import OAuth2
import json
from json import dumps, loads
from datetime import datetime
from pathlib import Path

class Yahoo_Api():
    def __init__(self, consumer_key, consumer_secret,
                access_key):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_key = access_key
        self._authorization = None
    def _login(self):
        global oauth
        oauth = OAuth2(None, None, from_file='./auth/oauth2yahoo.json')
        if not oauth.token_is_valid():
            oauth.refresh_access_token()

class ConvertJson():

# Used to parse the data received from the API for the current standings.
# Receives rank for the ordered standings, based on the rank. Needs to order by rank when starts.
# Receives name for the standings in alphabetical order
    def StandingsParse(json, orderby):
        aux = json[1]['standings'][0]['teams'] #[i]['team'] to iterate through all teams
        teams = []
        for i in range(num_teams):
            team = {
            "Name": aux[str(i)]['team'][0][2]['name'],
            "Team logo": aux[str(i)]['team'][0][5]['team_logos'][0]['team_logo']['url'],
            "Nickname": aux[str(i)]['team'][0][19]['managers'][0]['manager']['nickname'],
            #"Rank": int(aux[str(i)]['team'][2]['team_standings']['rank']),
            "Rank": aux[str(i)]['team'][2]['team_standings']['rank'],
            "Wins": int(aux[str(i)]['team'][2]['team_standings']['outcome_totals']['wins']),
            "Losses": int(aux[str(i)]['team'][2]['team_standings']['outcome_totals']['losses']),
            "Percentage": aux[str(i)]['team'][2]['team_standings']['outcome_totals']['percentage'],
            #"Percentage": float(aux[str(i)]['team'][2]['team_standings']['outcome_totals']['percentage']),
            "Points For": float(aux[str(i)]['team'][2]['team_standings']['points_for']),
            "Points Against": float(aux[str(i)]['team'][2]['team_standings']['points_against']),
            }
            teams.append(team)

        if orderby == 'rank': #If order by rank
            data = {
                "current_week": json[0]['current_week'], #works
                "Last Updated": datetime.now().strftime("%d/%m/%y %H:%M:%S"), #works
                "standings": sorted(teams, key=lambda x: (-x['Wins'], -x['Points For'])) #works, order by percentage when league starts

            }
        else:
            data = {
                "current_week": json[0]['current_week'], #works
                "Last Updated": datetime.now().strftime("%d/%m/%y %H:%M:%S"), #works
                "standings": sorted(teams, key=lambda x: x['Nickname']) #works
            }

        return data

# Used to parse the data received from the API for the transactions. Works
    def TransactionsParse(json):
        transactions = []
        for i in range(json[1]['transactions']['count']):
            if(json[1]['transactions'][str(i)]['transaction'][0]['type'] != "commish"):
                players = []
                for j in range(json[1]['transactions'][str(i)]['transaction'][1]['players']['count']):
                    player = {
                        "Name": json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][0][2]['name']['full'],
                        "Positions": json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][0][4]['display_position'],
                    }
                    if isinstance(json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data'], list):
                        player['Source type'] = json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data'][0]['source_type']
                        player['Destination type'] = json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data'][0]['destination_type']
                        if player['Destination type'] == "team":
                            player['Destination'] = json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data'][0]['destination_team_name']
                        else:
                            player['Destination'] = "Free Agent"

                        if player['Source type'] == "team":
                            player['Source'] = json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data'][0]['source_team_name']
                        else:
                            player['Source'] = "Free Agent"
                            
                    else:
                        player['Source type'] = json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data']['source_type']
                        player['Destination type'] = json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data']['destination_type']
                        if player['Destination type'] == "team":
                            player['Destination'] = json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data']['destination_team_name']
                        else:
                            player['Destination'] = "Free Agent"

                        if player['Source type'] == "team":
                            player['Source'] = json[1]['transactions'][str(i)]['transaction'][1]['players'][str(j)]['player'][1]['transaction_data']['source_team_name']
                        else:
                            player['Source'] = "Free Agent"

                    players.append(player)
                transaction= {
                    "Type": json[1]['transactions'][str(i)]['transaction'][0]['type'], #works
                    "Players": players
                }
                transactions.append(transaction)
        data = {
            "Last Updated": datetime.now().strftime("%d/%m/%y %H:%M:%S"), #works
            "Transactions": transactions
        }
        return data
        
# Used to parse the data received from the API for the free agents. Works
    def FreeAgentsParse(json):
        players = []
        for i in range(len(json[1]['players'])-1):
            player = {
                "Name": json[1]['players'][str(i)]['player'][0][2]['name']['full'], #works
            }
            #Some player have positions and teams on different positions
            for j in range(5, len(json[1]['players'][str(i)]['player'][0]) - 1):
                if(type(json[1]['players'][str(i)]['player'][0][j]) is dict):
                    if(list(json[1]['players'][str(i)]['player'][0][j].keys())[0] == 'editorial_team_full_name'):
                        player['Team'] = json[1]['players'][str(i)]['player'][0][j]['editorial_team_full_name']
                    elif (list(json[1]['players'][str(i)]['player'][0][j].keys())[0] == 'display_position'):
                        player['Positions'] = json[1]['players'][str(i)]['player'][0][j]['display_position']

            players.append(player)
        return players

# Used to parse the data received from the API for the draft prospects. Should need no rework.
    def DraftParse(json, number):
        players = []
        for i in range(number):
            player = {
                "Name": json[1]['players'][str(i)]['player'][0][2]['name']['full'], #works
                "Average pick": float(json[1]['players'][str(i)]['player'][1]['draft_analysis'][0]['average_pick']) #works
            }
            players.append(player)
        return players

# Used to parse the data received from the API for the league schedule.
# Should work
    def ScheduleParse(json):
        matches = []
        for i in range(6):
            match = {
                "Team1": json[1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams']['0']['team'][0][2]['name'],
                "Team1 Points": float(json[1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams']['0']['team'][1]['team_points']['total']),
                "Team1 Matches": json[1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams']['0']['team'][1]['team_remaining_games']['total']['remaining_games'],
                "Team1 Projected": json[1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams']['0']['team'][1]['team_projected_points']['total'],

                "Team2": json[1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams']['1']['team'][0][2]['name'],
                "Team2 Points": float(json[1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams']['1']['team'][1]['team_points']['total']),
                "Team2 Matches": json[1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams']['1']['team'][1]['team_remaining_games']['total']['remaining_games'],
                "Team2 Projected": json[1]['scoreboard']['0']['matchups'][str(i)]['matchup']['0']['teams']['1']['team'][1]['team_projected_points']['total'],
            }
            matches.append(match)

        Schedule = {
            "Week": int(json[1]['scoreboard']['week']),
            "Playoffs": json[1]['scoreboard']['0']['matchups']['0']['matchup']['is_playoffs'],
            "Matches": matches
        }
        return Schedule


# Used to parse the data received from the API for the rosters. 
# Works
    def RosterParse(json):
        players = []
        for i in range(len(json[1]['roster']['0']['players']) - 1):
            player = {
                "Name": json[1]['roster']['0']['players'][str(i)]['player'][0][2]['name']['full'], 
            }
            #Some player have positions and teams on different positions
            for j in range(5, len(json[1]['roster']['0']['players'][str(i)]['player'][0]) - 1):
                if(type(json[1]['roster']['0']['players'][str(i)]['player'][0][j]) is dict):
                    if(list(json[1]['roster']['0']['players'][str(i)]['player'][0][j].keys())[0] == 'editorial_team_full_name'):
                        player['Team'] = json[1]['roster']['0']['players'][str(i)]['player'][0][j]['editorial_team_full_name']
                    elif (list(json[1]['roster']['0']['players'][str(i)]['player'][0][j].keys())[0] == 'display_position'):
                        player['Positions'] = json[1]['roster']['0']['players'][str(i)]['player'][0][j]['display_position']

            players.append(player)
        team = {
            "Name": json[0][2]['name'], #works
            "Team logo": json[0][5]['team_logos'][0]['team_logo']['url'], #works
            "Nickname": json[0][19]['managers'][0]['manager']['nickname'], #works
            "players": players #check
        }
        return team

class UpdateData():
    def __init__(self):
        print("init")

# Function to update the league standings. Makes the request to the API, parses data via StadingsParse and adds to the json file.
# Should work properly.
    def UpdateLeagueStandings(self):
        # STANDINGS
        yahoo_api._login()
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/standings'
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()

        data = ConvertJson.StandingsParse(r['fantasy_content']['league'], 'rank') #Gets stadings ordered by rank
        
        with open(storage_path + "/standings/standings.json", 'w') as outfile: 
            json.dump(data, outfile) #stores in standings.json file
        
        return

# Function to update the league monthly standing. 
# Makes the request to the API, parses data via MonthlyStadingsParse and adds to the json file.
    def UpdateMonthlyStandings(self):
        yahoo_api._login()
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/standings'
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()

        data = ConvertJson.StandingsParse(r['fantasy_content']['league'], 'name') ##Gets stadings in alphabetical order
        path = storage_path + "/standings/start.json" #defines the path to the file containing start of the month stadings

        if(datetime.now().strftime("%d") == '1'): #if its the first day of the month, change start rank
            with open(path, 'w') as outfile:
                json.dump(data, outfile) #stores current stadings in start.json

        load_file = open(path) # load start.json
        start = json.load(load_file) # loads start of the month standings from start.json
        load_file.close()
        start['standings'] = sorted(start['standings'], key=lambda x: x['Nickname'])
        #for all 12 teams, subtract current statistics from the ones at the start of the month, getting stats from this month
        for i in range(12):
            data['standings'][i]['Wins'] -= start['standings'][i]['Wins'] #Current wins - wins at start of the month
            data['standings'][i]['Losses'] -= start['standings'][i]['Losses'] 
            data['standings'][i]['Points For'] -= start['standings'][i]['Points For']
            data['standings'][i]['Points For'] = round(data['standings'][i]['Points For'], 1)
            data['standings'][i]['Points Against'] -= start['standings'][i]['Points Against']
            if(data['standings'][i]['Wins'] == 0): #Has no wins
                data['standings'][i]['Percentage'] = 0
            elif(data['standings'][i]['Losses'] == 0): #Has wins, but no losses
                data['standings'][i]['Percentage'] = 100
            else: #Has wins and losses, calculate percentage
                data['standings'][i]['Percentage'] = (data['standings'][i]['Wins'] * 100)/(data['standings'][i]['Wins']+data['standings'][i]['Losses'])

        data = sorted(data['standings'], key=lambda x: (-x['Wins'], -x['Points For'])) # sort by wins. Should be percentage and points for
        for i in range(12):
            data[i]['Rank'] = str(i+1)
        with open(storage_path + "/standings/" + datetime.now().strftime("%b") + '.json', 'w') as outfile:
            json.dump(data, outfile) #Stores the data from this months standings on "name of the month".json
        return
    
# Function to update the league transactions. Makes the request to the API, parses data via TransactionsParse and adds to the json file.
    def UpdateLeagueTransactions(self):
        yahoo_api._login()
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/transactions'
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()

        data = ConvertJson.TransactionsParse(r['fantasy_content']['league'])
        path = storage_path + '/transactions/Transactions.json' # define path to the file containing the transactions

        if Path(path).is_file(): #Makes sure that transactions.json exists
            load_file = open(path) # load old_transactions
            old_transactions = json.load(load_file)
            new = data['Transactions'][0:len(data['Transactions']) - len(old_transactions['Transactions'])] #New transactions = new transactions - old transactions
            load_file.close()
        with open(path, 'w') as outfile:
            json.dump(data, outfile) #stores all transactions in transactions.json

        with open(storage_path + '/transactions/newTransactions.json', 'w') as newTransactions:
            json.dump(new, newTransactions) #stores new transactions in newTransactions.json
        return

# Function to update the league´s top free agents. Makes the request to the API, parses data via FreeAgentsParse and adds to the json file.
# Works
    def UpdateFreeAgents(self):
        yahoo_api._login()
        qtd = 15 # Ammount of free agents pulled from API
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/players;status=FA;sort=AR;count='+ str(qtd)
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()
        data = ConvertJson.FreeAgentsParse(r['fantasy_content']['league'])

        path = storage_path + '/freeagents/FreeAgents.json' # define path to the file containing the free agents
        with open(path, 'w') as outfile:
            json.dump(data, outfile) #stores the free agents in FreeAgents.json
        return

# Function to update the league´s top players. Makes the request to the API, parses data via FreeAgentsParse and adds to the json file.
    def UpdateMVP(self):
        yahoo_api._login()
        qtd = 15 # Ammount of free agents pulled from API
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/players;sort=AR;count='+ str(qtd)
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()
        data = ConvertJson.FreeAgentsParse(r['fantasy_content']['league'])

        path = storage_path + '/awardrace/MVP.json' # define path to the file containing the free agents
        with open(path, 'w') as outfile:
            json.dump(data, outfile) #stores the free agents in FreeAgents.json
        return

# Function to update the rosters. Makes the request to the API, parses data via RostersParse and adds to the json file.
# Works.
    def UpdateRosters(self):
        yahoo_api._login()
        data = [] #receives all the data
        #Needs one request per roster, takes a while.
        for i in range(1, 13):
            url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/'+game_key+'.l.'+league_id+'.t.' + str(i) + '/roster'
            response = oauth.session.get(url, params={'format': 'json'})
            r = response.json()
            data.append(ConvertJson.RosterParse(r['fantasy_content']['team'])) #Add roster info to data

        data = sorted(data, key=lambda x: x['Name'])
        path = storage_path + '/rosters/Rosters.json' # define path to the file containing the rosters
        with open(path, 'w') as outfile:
            json.dump(data, outfile) #stores the rosters in Rosters.json
        return


# Function to update the schdule. Makes the request to the API, parses data via ScheduleParse and adds to the json file.
# Should work.
    def UpdateSchedule(self):
        yahoo_api._login()
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/scoreboard'
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()
        data = ConvertJson.ScheduleParse(r['fantasy_content']['league'])

        with open('Schedule.json', 'w') as outfile:
            json.dump(data, outfile) #stores the Schedule in Schedule.json
        
        if(datetime.today().strftime('%A') == 'Monday'):
            week = str(data['Week'] - 1)
            url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/scoreboard;week='+week
            response = oauth.session.get(url, params={'format': 'json'})
            r = response.json()
            data = ConvertJson.ScheduleParse(r['fantasy_content']['league'])

            with open('PrevSchedule.json', 'w') as outfile:
                json.dump(data, outfile) #stores the Schedule from the past week in PrevSchedule.json

        return



# Function to get a mock draft. Makes the request to the API, parses data via DraftParse and adds to the json file.
# Works properly. Will not be used during the season. Pre season only, for bot tweet.
    def MockDraft(self):
        data = [] #receives all the data
        yahoo_api._login()
        #One request can only take up to 25, so needs a few. Was bugged with 25, so switched to 14 and it worked
        for i in range(13):
            url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/players;status=FA;sort=OR;count=13;start=' + str(i * 13) +'/draft_analysis'
            response = oauth.session.get(url, params={'format': 'json'})
            r = response.json()
            data += ConvertJson.DraftParse(r['fantasy_content']['league'], 13)

        data = sorted(data, key = lambda x: x['Average pick']) #Sorts all the data received based on average pick

        with open('MockDraft.json', 'w') as outfile:
            json.dump(data, outfile) #stores players in MockDraft.json
        return

# Used to define the game key
    def UpdateYahooLeagueInfo(self):
        # UPDATE LEAGUE GAME ID
        yahoo_api._login()
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/game/nba'
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()
        with open('YahooGameInfo.json', 'w') as outfile:
            json.dump(r, outfile)
            
        global game_key
        game_key = r['fantasy_content']['game'][0]['game_key'] # game key as type-string
        return

### WHERE ALL THE MAGIC HAPPENS #########

def main():
##### Get Yahoo Auth ####

    # Yahoo Keys
    with open('./auth/oauth2yahoo.json') as json_yahoo_file:
        auths = json.load(json_yahoo_file)
    yahoo_consumer_key = auths['consumer_key']
    yahoo_consumer_secret = auths['consumer_secret']
    yahoo_access_key = auths['access_token']
    #yahoo_access_secret = auths['access_token_secret']
    json_yahoo_file.close()

#### Declare Yahoo, and Current Week Variable ####


    global yahoo_api
    yahoo_api = Yahoo_Api(yahoo_consumer_key, yahoo_consumer_secret, yahoo_access_key)#, yahoo_access_secret)

    with open('./Initial_Setup/league_info_form.txt', 'r') as f:
        rosters = eval(f.read())

    global num_teams
    num_teams = rosters['num_teams']

    global num_weeks
    num_weeks = rosters['num_weeks']
    
    global league_id
    league_id = str(rosters['league_id'])

    global storage_path
    storage_path = './fantasytracker/src/Components/Data'

#### Where the tweets happen ####
    bot = Bot(yahoo_api)
    bot.run()


class Bot():
    def __init__(self, yahoo_api):
        self._yahoo_api = yahoo_api

    def run(self):
        # Data Updates
        UD = UpdateData()

        UD.UpdateYahooLeagueInfo()
        print('League Info update - Done')                   
        UD.UpdateLeagueStandings() #Works
        print('Standings update - Done') 
        UD.UpdateMonthlyStandings() #Works
        print('Monthly Standings update - Done')
        #UD.UpdateLeagueTransactions() #Works
        print('Transactions update - Done')
        UD.UpdateFreeAgents() #Works
        print('Free Agents update - Done')
        UD.UpdateMVP() #Works
        print('Free Agents update - Done')
        UD.UpdateSchedule() #Should work
        print('Schedule update - Done')
        #UD.MockDraft()
        #print('Draft update - Done')
        UD.UpdateRosters() #Works
        print('Rosters update - Done')
        print('Update Complete')

if __name__ == "__main__":
    main()

    try:
        pass
    except Exception as e:
        raise
    else:
        pass
