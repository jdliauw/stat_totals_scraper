import requests
import os
import shutil
from bs4 import BeautifulSoup
import time
# import HTMLParser

player_url = []
game_log_url = []

def run():
    years = []
    hold = []
    print '\n   This script pulls the totals stat table from basketball-reference.com'
    print '   for a given year/s and stores it to a new directory \'year_stats_files\' in the format:'
    print '   \"year_nba_totals.csv\"\n'
    print '   If you want to pull:'
    print '   * a single year, just type the year'
    print '   * from multiple years, separate each year by a space'
    print '   * from a range of years, separate by the years by a \'-\' (ex: 1996-1997)'

    print ''
    selection = raw_input("   Year(s) selection: ")

    if ' ' not in selection and '-' not in selection:
        years.append(selection)

    elif ' ' in selection:
        years = selection.split(' ')

        flag = True
        i = 0

        while flag:

            if '-' in years[i]:
                hold = years[i].split('-')

                for j in range(int(hold[1])  + 1 - int(hold[0])):
                    hold.append(str(int(hold[0]) + j))

                hold.remove(hold[0])
                hold.remove(hold[0])                

                for k in range(0, len(hold)):
                    if(hold[k] not in years):
                        years.append(hold[k])
                years.remove(years[i])
                i = i - 1

            i = i + 1

            if i == len(years):
                flag = False

    else:
        years = selection.split('-')

        for i in range(int(years[1]) + 1 - int(years[0])):
            years.append(str(int(years[0]) + i))

        years.remove(years[0])
        years.remove(years[0])
           
    years.sort()
    
    if not os.path.exists('year_stats_files'):
        os.makedirs('year_stats_files')
    
    source = os.path.dirname(os.path.abspath(__file__))
    year_destination = source + "/year_stats_files"
            
    try:
        for i in range(0, len(years)):
            store_league_year_stats(years[i])
            file_name = str(years[i]) + '_nba_totals.csv'
            shutil.move(file_name, year_destination)
            print '   + Successfully stored ' + str(years[i]) + '_nba_totals.csv'
    except:
        print '   - Failed to store ' + str(years[i]) + '_nba_totals.csv'

    print ''  
#
def store_league_year_stats(year):
    time.sleep(5)
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    url_request = requests.get(url)
    html = url_request.text
    output = open(str(year) + '_nba_totals.csv', "w+") 
    soup = BeautifulSoup(html, 'html.parser')
    stats_table = soup.find('table', {'class' : 'sortable  stats_table'}).find('tbody').findAll('tr')

    player_stats, all_stats = [], []
    all_stats.append(['PID','LAST', 'FIRST','POS', 'AGE', 'TEAM', 'GP', 'GS', 'MP', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', '2PM',
    '2PA', '2P%', 'EFG%', 'FTM', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])
    
    for row in stats_table:
        omit = 0
        for attribute in row.findAll('td'):
            if omit != 0:
                if omit == 1:
                    pid = attribute.find('a')['href']
                    pid = pid[pid.rfind('/') + 1 : pid.rfind('.')]
                    player_stats.append(pid)
                    name = attribute['csk']
                    last, first = name.split(',')
                    player_stats.append(last)
                    player_stats.append(first)
                else:
                    player_stats.append(attribute.string)
            omit = omit + 1
        
        if(len(player_stats) > 1):
            all_stats.append(player_stats)
        player_stats = []
        
    for i in range(0, len(all_stats)):
        for j in range(0, len(all_stats[i])):
            output.write(str(all_stats[i][j]))
            if j != len(all_stats[i])-1:
                output.write(',')
        output.write('\n')

    output.close()
#
def store_game_logs(player_url):
    # time.sleep(5)
    url_request = requests.get(player_url)
    html = url_request.text
    soup = BeautifulSoup(html, 'html.parser')
    pid = player_url[player_url.rfind('players') + 10 : -14]
    file_name = str(pid) + '_' + player_url[-5 : -1] + '_gamelog.csv'
    output = open(str(pid) + '_' + player_url[-5 : -1] + '_gamelog.csv', "w+")
    gl_table = soup.find('table', {'class' : 'sortable  row_summable stats_table'}).find('tbody').findAll('tr')

    game_stats, game_log = [], []

    game_log.append(['PID', 'GAME', 'DATE', 'AGE', 'TEAM', 'HOME/AWAY', 'OPP', 'RESULT', 'GS', 'MP', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 
    'FTM', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GMSC', '+/-', 'DFS'])

    for row in gl_table: 
        omit = 0
        for attribute in row.findAll('td'):
            if omit == 0:
                game_stats.append(pid)
            else:
                game_stats.append(attribute.string)
            omit = omit + 1
        
        if(len(game_stats) > 1 and game_stats[1] != None):
            game_log.append(game_stats)
        game_stats = []

    for i in range(0, len(game_log)):
        for j in range(0, len(game_log[i])):
            output.write(str(game_log[i][j]))
            if j != len(game_log[i])-1:
                output.write(',')
        output.write('\n')

    output.close()

    if not os.path.exists('game_logs'):
        os.makedirs('game_logs')
    
    if not os.path.exists('game_logs/' + pid):
        os.makedirs('game_logs/' + pid)

    source = os.path.dirname(os.path.abspath(__file__))
    destination = source + '/game_logs/' + pid
    shutil.move(file_name, destination)

#
def grab_player_urls(year):
    time.sleep(5)
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    url_request = requests.get(url)
    html = url_request.text
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find('table', {'class' : 'sortable  stats_table'}).find('tbody').findAll('a')
    
    for a_tag in a_tags:
        if 'players' in a_tag['href']:
            full_url = 'http://basketball-reference.com' + str(a_tag['href'])
            # if full_url not in player_url:            
            player_url.append(full_url)
#
def grab_game_log_urls(url):
    time.sleep(5)
    url_request = requests.get(url)
    html = url_request.text
    li_tags = BeautifulSoup(html, 'html.parser').findAll('li', {'class' : 'narrow'})
    a_tags = BeautifulSoup(str(li_tags), 'html.parser').findAll('a')
    del li_tags
    
    for a_tag in a_tags:
        if 'gamelog' in a_tag['href']:
            full_url = 'http://basketball-reference.com' + str(a_tag['href'])
            if full_url not in game_log_url:            
                game_log_url.append(full_url)
            
    for game_log in game_log_url:
        print str(game_log)
#

# ---------------- main ----------------

# run()
# grab_player_urls(2016)
# grab_game_log_urls(player_url[92])
# store_league_year_stats(2016)
store_game_logs('http://www.basketball-reference.com/players/c/conlemi01/gamelog/2015/')

'''

What's next:
    
    Overview:
    1. Grab player urls from totals table
    2. Grab game log urls from player page
    3. Store it via store_game_logs 

    Immediate:
    + Add directories/subdirectories to organize game_log files by player

    High priority:
    + Make postgres connection
    + Store data to database instead of csv
    + Generate PER 36 stats (why is it 36, not 48...too much extrapolation?) <--- do this within postgres db
    + Apply fantasy rules to calculate:
        + daily fpoints, 
        + year total fpoints, 
        + fpoints stddev,
        + average stddev amongst players (min minimum?)

    ---- At this point you have all the data you need ----

    Questions: 
    1. How to use data to make projections? Are average and stddev enough? 


    Low priority:
    1. Improve user interface

'''