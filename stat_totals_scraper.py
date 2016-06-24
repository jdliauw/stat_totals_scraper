import urllib
import requests
import HTMLParser
import os
import shutil
from bs4 import BeautifulSoup

def crawl_it(year):
    
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    url_response = requests.get(url)
    html = url_response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    output_file = open("soup.html", "w+")
    output_file.write(str(soup))
    output_file.close()

def log_it(year):
    html = open("soup.html")
    output = open(str(year) + '_NBA_TOTALS.csv', "w+")

    player_stats, all_stats = [], []
    all_stats.append(['LAST', 'FIRST','POS', 'AGE', 'TEAM', 'GP', 'GS', 'MP', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', '2PM',
    '2PA', '2P%', 'EFG%', 'FTM', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])

    bsoup = BeautifulSoup(html, 'html.parser')
    stats_table = bsoup.find('table', {'class' : 'sortable  stats_table'}).find('tbody').findAll('tr')

    for row in stats_table:
        omit = 0
        for attribute in row.findAll('td'):
            if omit != 0:

                if omit == 1:
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

def eww_gui():
    years = []
    hold = []
    print '\n   This script pulls the totals stat table from basketball-reference.com'
    print '   for a given year/s and stores it to your current directory in the format:'
    print '   \"YEAR_NBA_TOTALS.csv\"\n'
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
    
    if not os.path.exists('csv_files'):
        os.makedirs('csv_files')
    
    source = os.path.dirname(os.path.abspath(__file__))
    destination = source + "/csv_files"
            
    try:
        for i in range(0, len(years)):
            crawl_it(years[i])
            log_it(years[i])
            file_name = str(years[i]) + '_NBA_TOTALS.csv'
            shutil.move(file_name,destination)
            print '   + Successfully stored ' + str(years[i]) + '_NBA_TOTALS.csv'
    except:
        print '   - Failed to store ' + str(years[i]) + '_NBA_TOTALS.csv'

    print ''

# ---------------- main ----------------

eww_gui()