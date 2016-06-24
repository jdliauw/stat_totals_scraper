import urllib
import requests
import HTMLParser
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
    output = open(str(year) + '_stats.csv', "w+")

    player_stats, all_stats = [], []
    all_stats.append(['LAST', 'FIRST','POS', 'AGE', 'TEAM', 'GP', 'GS', 'MP', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'EFG%', 'FTM', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])

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
    indices = []
    hold = []
    print '\nThis script pulls the totals stat table from basketball-reference.com for a given year or years and stores it as a csv in your current directory in the format: \"YEAR_stats.csv\"\n'
    print '   + If you want to pull a single year, just type the year followed by \'enter\'\n   + If you want to pull from multiple years, separate each year by a space, then \'enter\'.'
    print '   + If you want to pull from a range of years, separate by the years by a \'-\' (ex: 1996-1997), then \'enter\'\n'

    selection = raw_input("   Year(s) selection: ")

    # input cases:
    '''
        1. single year
        2. multiple years separated by space
        3. multiple year and single range
        4. single year and multiple range
        5. multiple year and multiple range
    '''

    if ' ' not in selection and '-' not in selection:

        try:
            crawl_it(selection)
            log_it(selection)
            print '\n   **** Success:', selection, 'stat table stored as: \"' + selection + '_stats.txt\" ****\n'
        except:
            print '\n   **** Failed: invalid year input ****\n'

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
        
        for i in range(0, len(years)):
            crawl_it(years[i])
            log_it(years[i])

    print years
    

# ---------------- main ----------------

eww_gui()

# for year in range(2000, 2010):
#     crawl_it(year)
#     log_it(year)