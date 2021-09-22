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

# Used to parse the data received from the API for the current standings. Needs small rework to use percentage once they exist.
    def StandingsParse(json):
        aux = json[1]['standings'][0]['teams'] #[i]['team'] to iterate through all teams
        teams = []
        for i in range(num_teams):
            team = {"Name": aux[str(i)]['team'][0][2]['name'],
            "Team logo": aux[str(i)]['team'][0][5]['team_logos'][0]['team_logo']['url'],
            "Nickname": aux[str(i)]['team'][0][19]['managers'][0]['manager']['nickname'],
            "Rank": aux[str(i)]['team'][2]['team_standings']['rank'],
            "Wins": int(aux[str(i)]['team'][2]['team_standings']['outcome_totals']['wins']),
            "Losses": int(aux[str(i)]['team'][2]['team_standings']['outcome_totals']['losses']),
            "Percentage": aux[str(i)]['team'][2]['team_standings']['outcome_totals']['percentage'],
            #"Percentage": float(aux[str(i)]['team'][2]['team_standings']['outcome_totals']['percentage']),
            "Points For": float(aux[str(i)]['team'][2]['team_standings']['points_for']),
            "Points Against": float(aux[str(i)]['team'][2]['team_standings']['points_against']),
            }
            teams.append(team)
        #print(sorted(teams, key=lambda x: (-x['Percentage'], ['Points For'])))

        data = {
            "current_week": json[0]['current_week'], #works
            "Last Updated": datetime.now().strftime("%d/%m/%y %H:%M:%S"), #works
            "standings": sorted(teams, key=lambda x: (-x['Wins'], ['Points For'])) #works, order by percentage when league starts

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
            "Number Of Transactions": json[1]['transactions']['count'],
            "Last Updated": datetime.now().strftime("%d/%m/%y %H:%M:%S"), #works
            "Transactions": transactions
        }
        return data

    def FreeAgentsParse(json, number):
        players = []
        for i in range(number):
            player = {
                "Name": json[1]['players'][str(i)]['player'][0][2]['name']['full'],
                "Team": json[1]['players'][str(i)]['player'][0][5]['editorial_team_full_name'],
                "Positions": json[1]['players'][str(i)]['player'][0][8]['display_position']
            }
            players.append(player)
        return players

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
        data = ConvertJson.StandingsParse(r['fantasy_content']['league'])
        week = data['current_week']
        print(storage_path + '/standings/week'+ week + ".json")
        with open(storage_path + '/standings/week'+ week + ".json", 'w') as outfile:
            json.dump(data, outfile)
        
        return
    
# Function to update the league transactions. Makes the request to the API, parses data via TransactionsParse and adds to the json file.
# Needs rework once real transactions are made.
    def UpdateLeagueTransactions(self):
        yahoo_api._login()
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/transactions'
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()
        data = ConvertJson.TransactionsParse(r['fantasy_content']['league'])
        path = storage_path + '/transactions/Transactions.json'
        new = data
        if Path(path).is_file():
            load_file = open(path) # load old_transactions
            old_transactions = json.load(load_file)
            new = dict(set(data) - set(old_transactions))
            load_file.close()
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
        with open(storage_path + '/transactions/newTransactions.json', 'w') as newTransactions:
            json.dump(new, newTransactions)
        return

# Function to update the league´s top free agents. Makes the request to the API, parses data via FreeAgentsParse and adds to the json file.
# Should work properly, could change qtd for a bigger list.
    def UpdateFreeAgents(self):
        yahoo_api._login()
        qtd = 5
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/'+game_key+'.l.'+league_id+'/players;status=FA;sort=OR;count='+ str(qtd)
        response = oauth.session.get(url, params={'format': 'json'})
        r = response.json()
        data = ConvertJson.FreeAgentsParse(r['fantasy_content']['league'], qtd)
        path = storage_path + '/freeagents/FreeAgents.json'
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
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
        #UD.UpdateLeagueStandings()
        print('Standings update - Done')
      #  UD.UpdateLeagueTransactions()
        print('Transactions update - Done')
        UD.UpdateFreeAgents()
        print('Free Agents update - Done')
                                        
        print('Update Complete')

if __name__ == "__main__":
    main()

    try:
        pass
    except Exception as e:
        raise
    else:
        pass
