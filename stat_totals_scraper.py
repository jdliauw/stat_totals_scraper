import urllib
import requests
import HTMLParser
from bs4 import BeautifulSoup

def crawl_it(year):
    
    # assign url
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    
    # store requests module response from url
    url_response = requests.get(url)
    
    # store the text field of url_response
    html = url_response.text
    
    # store as a Beautiful Soup object the parsed HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    html_text = soup
    
    output_file = open("soup.html", "w+")
    output_file.write(str(soup))
    output_file.close()


def log_it(year):
    html = open("soup.html")
    output = open(str(year) + '_stats.txt', "w+")

    player_stats, all_stats = [], []
    all_stats.append(['FIRST', 'LAST','POS', 'AGE', 'TEAM', 'GP', 'GS', 'MP', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'EFG%', 'FTM', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])

    bsoup = BeautifulSoup(html, 'html.parser')
    stats_table = bsoup.find('table', {'class' : 'sortable  stats_table'}).find('tbody').findAll('tr')

    for row in stats_table:
        omit = 0
        for attribute in row.findAll('td'):
            if omit != 0:

                if omit == 1:
                    name = attribute['csk']
                    last, first = name.split(',')
                    player_stats.append(first)
                    player_stats.append(last)
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

# ---------------- main ----------------

for year in range(1997, 1998):
    # crawl_it(year)
    log_it(year)