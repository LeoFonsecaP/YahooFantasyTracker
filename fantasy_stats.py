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
                "standings": sorted(teams, key=lambda x: x['Wins']) #works, order by percentage when league starts

            }
        else:
            data = {
                "current_week": json[0]['current_week'], #works
                "Last Updated": datetime.now().strftime("%d/%m/%y %H:%M:%S"), #works
                "standings": sorted(teams, key=lambda x: x['Name']) #works
            }

        return data

# Used to parse the data received from the API for the transactions. Needs rework once real transactions are made and
# I have a real understanding of how the data is returned.
    def TransactionsParse(json):
        transactions = []
        for i in range(json[1]['transactions']['count']):
            transaction= {
                "id": json[1]['transactions'][str(i)]['transaction'][0]['transaction_id'], #works
                "type": json[1]['transactions'][str(i)]['transaction'][0]['type'], #works
                }
            transactions.append(transaction)
        data = {
            "Number Of Transactions": json[1]['transactions']['count'], #make sure no weird transactions
            "Last Updated": datetime.now().strftime("%d/%m/%y %H:%M:%S"), #works
            "Transactions": transactions
        }
        return data
        
# Used to parse the data received from the API for the free agents. Should need no rework.
    def FreeAgentsParse(json, number):
        players = []
        for i in range(number):
            player = {
                "Name": json[1]['players'][str(i)]['player'][0][2]['name']['full'], #works
                "Team": json[1]['players'][str(i)]['player'][0][5]['editorial_team_full_name'], #works
                "Positions": json[1]['players'][str(i)]['player'][0][8]['display_position'] #works
            }
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

# Used to parse the data received from the API for the rosters. 
# Should need reword to add the players, commented section should be close.
    def RosterParse(json):
        #players = []
        #for i in range(number):
            #player = {
                #"Name": json[1]['players'][str(i)]['player'][0][2]['name']['full'], 
                #"Team": json[1]['players'][str(i)]['player'][0][5]['editorial_team_full_name'], 
                #"Positions": json[1]['players'][str(i)]['player'][0][8]['display_position']
            #}
            #players.append(player)
        team = {
            "Name": json[0][2]['name'], #works
            "Team logo": json[0][5]['team_logos'][0]['team_logo']['url'], #works
            "Nickname": json[0][19]['managers'][0]['manager']['nickname'], #works
            "players": json[1]['roster']['0']['players'] #check
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

        #for all 12 teams, subtract current statistics from the ones at the start of the month, getting stats from this month
        for i in range(12): 
            data['standings'][i]['Wins'] -= start['standings'][i]['Wins'] #Current wins - wins at start of the month
            data['standings'][i]['Losses'] -= start['standings'][i]['Losses'] 
            data['standings'][i]['Points For'] -= start['standings'][i]['Points For']
            data['standings'][i]['Points Against'] -= start['standings'][i]['Points Against']
            if(data['standings'][i]['Wins'] == 0): #Has no wins
                data['standings'][i]['Percentage'] = 0
            elif(data['standings'][i]['Losses'] == 0): #Has wins, but no losses
                data['standings'][i]['Percentage'] = 100
            else: #Has wins and losses, calculate percentage
                data['standings'][i]['Percentage'] = (data['standings'][i]['Wins'] * 100)/(data['standings'][i]['Wins']+data['standings'][i]['Losses'])
        
        data = sorted(data['standings'], key=lambda x: -x['Wins']) # sort by wins. Should be percentage and points for
        with open(storage_path + "/standings/" + datetime.now().strftime("%b") + '.json', 'w') as outfile:
            json.dump(data, outfile) #Stores the data from this months standings on "name of the month".json
        return
    
# Function to update the league transactions. Makes the request to the API, parses data via TransactionsParse and adds to the json file.
# Needs rework once real transactions are made.
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
            new = dict(set(data) - set(old_transactions)) #New transactions = new transactions - old transactions
            load_file.close()

        with open(path, 'w') as outfile:
            json.dump(data, outfile) #stores all transactions in transactions.json

        with open(storage_path + '/transactions/newTransactions.json', 'w') as newTransactions:
            json.dump(new, newTransactions) #stores new transactions in newTransactions.json
        return

# Function to update the league´s top free agents. Makes the request to the API, parses data via FreeAgentsParse and adds to the json file.
# Should work properly, could change qtd for a bigger list.
    def UpdateFreeAgents(self):
        yahoo_api._login()
        qtd = 15 # Ammount of free agents pulled from API
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/players;status=FA;sort=OR;count='+ str(qtd)
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()

        data = ConvertJson.FreeAgentsParse(r['fantasy_content']['league'], qtd)

        path = storage_path + '/freeagents/FreeAgents.json' # define path to the file containing the free agents
        with open(path, 'w') as outfile:
            json.dump(data, outfile) #stores the free agents in FreeAgents.json
        return

# Function to update the rosters. Makes the request to the API, parses data via RostersParse and adds to the json file.
# Should work, need to get the player data after the draft.
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
        UD.UpdateLeagueStandings()
        print('Standings update - Done') 
        UD.UpdateMonthlyStandings()
        print('Monthly Standings update - Done')
        UD.UpdateLeagueTransactions()
        print('Transactions update - Done')
        UD.UpdateFreeAgents()
        print('Free Agents update - Done')
        #UD.MockDraft()
        #print('Draft update - Done')
        UD.UpdateRosters()
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
