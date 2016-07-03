import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import shutil
import time

start = time.time()
# connection = psycopg2.connect(database="nba_stats_db", host="127.0.0.1", port="5432")
# cursor = connection.cursor()

player_url = []
game_log_url = []

def create_table():
    cursor.execute('''
    CREATE TABLE "game_logs"
    ("pid" TEXT,
    "first" TEXT,
    "last" TEXT,
    "game" INT,
    "year" INT,
    "month" INT,
    "day" INT,
    "age" REAL,
    "team" TEXT,
    "home/away" TEXT,
    "opp" TEXT,
    "result" INT,
    "gs" BOOLEAN,
    "mp" REAL,
    "fgm" INT,
    "fga" INT,
    "fg%" REAL,
    "3pm" INT,
    "3pa" INT, 
    "3p%" REAL,
    "ftm" INT,
    "fta" INT,
    "ft%" REAL,
    "orb" INT,
    "drb" INT,
    "trb" INT,
    "ast" INT,
    "stl" INT,
    "blk" INT,
    "tov" INT,
    "pf" INT,
    "gmsc" REAL,
    "+/-" INT)
    ''')

    connection.commit()

def store_game_logs(player_gl_url, db = 1):
    # time.sleep(5)
    url_request = requests.get(player_gl_url)
    html = url_request.text
    soup = BeautifulSoup(html, 'html.parser')
    pid = player_gl_url[player_gl_url.rfind('players') + 10 : -14]
    gl_table = soup.find('table', {'class' : 'sortable  row_summable stats_table'}).find('tbody').findAll('tr')
    first, last = soup.find('h1').string.rsplit(' ',3)[0].split(' ',1)
    season = str(int(player_gl_url[-5:-1])-1) + '-' + str(player_gl_url[-5 : -1])

    if db == 0:
        file_name = str(pid) + '_' + player_gl_url[-5 : -1] + '_gamelog.csv'
        output
        output = open(str(pid) + '_' + player_gl_url[-5 : -1] + '_gamelog.csv', "w+")
        output.write('PID,FIRST,LAST,SEASON,GAME,YEAR,MONTH,DAY,AGE,TEAM,HOME/AWAY,OPP,RESULT,GS,MP,FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,GMSC,+/-\n')

        for row in gl_table: 
            glt_index = 0
            for attribute in row.findAll('td'):
                if glt_index == 0:
                    hold = attribute.string
                elif glt_index == 1:
                    if attribute.string == None:
                        glt_index = 0
                        break;
                    else:
                        output.write(pid + ',' + first + ',' + last + ',' + season + ',' + hold + ',')
                        glt_index = glt_index + 1
                        continue;
                elif glt_index == 2:
                    year, month, day = attribute.string.split('-')
                    output.write(year + ',' + month + ',' + day + ',')
                elif glt_index == 3:
                    years = attribute.string.split('-')
                    days = float(years[1])/365.25
                    years = float(years[0]) + float(days)
                    output.write(str(years) + ',')
                elif glt_index == 5:
                    if attribute.string == '@':
                       output.write('AWAY' + ',') 
                    else:
                        output.write('HOME' + ',')
                elif glt_index == 7:
                    if 'W' in attribute.string:
                        w = attribute.string[attribute.string.find('+') + 1 : attribute.string.rfind(')')]
                        output.write(w + ',')
                    else:
                        l = attribute.string[attribute.string.find('-') : attribute.string.rfind(')')]
                        output.write(l + ',')
                elif glt_index == 8:
                    if attribute.string == '1':
                        output.write('TRUE' + ',')
                    else:
                        output.write('FALSE' + ',')
                elif glt_index == 9:
                    mp = attribute.string.split(':')
                    if len(mp) == 3:
                        mp = float(mp[0]) + float(mp[1])/60 + float(mp[2])/360
                        output.write(str(mp) + ',')
                    else:
                        mp = float(mp[0]) + float(mp[1])/60
                        output.write(str(mp) + ',')
                elif glt_index == 29:
                    output.write(str(attribute.string) +'\n')
                    break;
                else:
                    output.write(str(attribute.string) + ',')
                glt_index = glt_index + 1

        output.close()
        
        if not os.path.exists('game_logs/' + pid):
            os.makedirs('game_logs/' + pid)

        source = os.path.dirname(os.path.abspath(__file__))
        gl_destination = source + '/game_logs/' + pid
        file_path = gl_destination + '/' + file_name
        if os.path.exists(file_path):
            os.remove(file_path) # write over file
        shutil.move(file_name, gl_destination)

    # else:
    #     for row in gl_table: 
    #         glt_index = 0
    #         for attribute in row.findAll('td'):
    #             if glt_index == 0:
    #                 hold = attribute.string
    #             elif glt_index == 1:
    #                 if attribute.string == None:
    #                     glt_index = 0
    #                     break;
    #                 else:
    #                     # output.write(pid + ',' + first + ',' + last + ',' + hold + ',')
    #                     glt_index = glt_index + 1
    #                     continue;
    #             elif glt_index == 2:
    #                 year, month, day = attribute.string.split('-')
    #                 # output.write(year + ',' + month + ',' + day + ',')
    #             elif glt_index == 3:
    #                 years = attribute.string.split('-')
    #                 days = float(years[1])/365.25
    #                 years = float(years[0]) + float(days)
    #                 # output.write(str(years) + ',')
    #             elif glt_index == 5:
    #                 if attribute.string == '@':
    #                    # output.write('AWAY' + ',') 
    #                 else:
    #                     # output.write('HOME' + ',')
    #             elif glt_index == 7:
    #                 if 'W' in attribute.string:
    #                     w = attribute.string[attribute.string.find('+') + 1 : attribute.string.rfind(')')]
    #                     # output.write(w + ',')
    #                 else:
    #                     l = attribute.string[attribute.string.find('-') : attribute.string.rfind(')')]
    #                     # output.write(l + ',')
    #             elif glt_index == 8:
    #                 if attribute.string == '1':
    #                     # output.write('TRUE' + ',')
    #                 else:
    #                     # output.write('FALSE' + ',')
    #             elif glt_index == 9:
    #                 mp = attribute.string.split(':')
    #                 if len(mp) == 3:
    #                     mp = float(mp[0]) + float(mp[1])/60 + float(mp[2])/360
    #                     # output.write(str(mp) + ',')
    #                 else:
    #                     mp = float(mp[0]) + float(mp[1])/60
    #                     # output.write(str(mp) + ',')
    #             elif glt_index == 29:
    #                 # output.write(str(attribute.string) +'\n')
    #                 break;
    #             else:
    #                 # output.write(str(attribute.string) + ',')
    #             glt_index = glt_index + 1

def grab_player_urls(year):
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    url_request = requests.get(url)
    html = url_request.text
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find('table', {'class' : 'sortable  stats_table'}).find('tbody').findAll('a')
    
    for a_tag in a_tags:
        if 'players' in a_tag['href']:
            full_url = 'http://basketball-reference.com' + str(a_tag['href'])
            if full_url not in player_url:            
                player_url.append(full_url)
#
def grab_game_log_urls(player_url):
    time.sleep(5)
    url_request = requests.get(player_url)
    html = url_request.text
    li_tags = BeautifulSoup(html, 'html.parser').findAll('li', {'class' : 'narrow'})
    a_tags = BeautifulSoup(str(li_tags), 'html.parser').findAll('a')
    del li_tags
    
    for a_tag in a_tags:
        if 'gamelog' in a_tag['href']:
            full_url = 'http://basketball-reference.com' + str(a_tag['href'])
            if full_url not in game_log_url:            
                game_log_url.append(full_url)
#

# ---------------- main ----------------

# create_table()
# grab_player_urls(2016)
# for i in range(len(player_url)):
    # grab_game_log_urls(player_url[i])
    # for j in range(len(game_log_url)):
        # store_game_logs(game_log_url)

store_game_logs('http://www.basketball-reference.com/players/c/conlemi01/gamelog/2016/', 0)

# connection.close()
print '\n*------------------------------*\n| time elapsed:', time.time() - start, ' |\n*------------------------------*\n'

'''
What's next:

    High priority:
    + Store data to database
    + Add daily fpoints column
    + Calculate
        + year total fpoints,
        + fpoints stddev,
        + player average fpoints stddev (min minimum?)

    ---- At this point you have all the data you need ----

    Low priority:
    1. Improve user interface

'''

def store_year_stats(year, db = 1):
    # time.sleep(5)
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    url_request = requests.get(url)
    html = url_request.text
    soup = BeautifulSoup(html, 'html.parser')
    stats_table = soup.find('table', {'class' : 'sortable  stats_table'}).find('tbody').findAll('tr')

    if db == 0:
        file_name = str(year) + '_nba_totals.csv'
        output = open(str(year) + '_nba_totals.csv', "w+") 
        output.write('PID,LAST,FIRST,POS,AGE,TEAM,GP,GS,MP,FGM,FGA,FG%,3PM,3PA,3P%,2PM,2PA,2P%,EFG%,FTM,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS\n')
    
        for row in stats_table:
            omit = 0
            for attribute in row.findAll('td'):
                if omit != 0:
                    if omit == 1:
                        pid = attribute.find('a')['href']
                        pid = pid[pid.rfind('/') + 1 : pid.rfind('.')]
                        output.write(pid + ',')
                        name = attribute['csk']
                        last, first = name.split(',')
                        output.write(last + ',')
                        output.write(first + ',')
                        del first, last, name
                    elif omit == 29:
                        output.write(str(attribute.string) + '\n')
                    else:
                        output.write(str(attribute.string) + ',')
                omit = omit + 1
            
        output.close()

        if not os.path.exists('year_stats_files'):
            os.makedirs('year_stats_files')
        
        source = os.path.dirname(os.path.abspath(__file__))
        year_destination = source + "/year_stats_files"
        file_path = year_destination + '/' + file_name
        if os.path.exists(file_path):
            os.remove(file_path) # write over file
        shutil.move(file_name, year_destination)

    else:
        pass

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
    
    try:
        for i in range(0, len(years)):
            store_year_stats(years[i])
            print '   + Successfully stored ' + str(years[i]) + '_nba_totals.csv'
    except:
        print '   - Failed to store ' + str(years[i]) + '_nba_totals.csv'

    print ''  
