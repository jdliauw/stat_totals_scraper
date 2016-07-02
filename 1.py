# first, last = soup.find('h1').string.rsplit(' ',3)[0].split(' ',1)

# --------------------------------------------------------------------------------

# ORIGINAL: PID,GAME,DATE,AGE,TEAM,HOME/AWAY,OPP,RESULT,GS,MP,FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,GMSC, +/-
# MOD: 0 PID, 1 FIRST, 2 LAST, 3 GAME, 4 DATE, 5 AGE, 6 TEAM, 7 HOME/AWAY, 8 OPP, 9 RESULT, 10 GS, 11 MP, 12 FGM, 13 FGA, 14 FG%, 15 3PM,
#      16 3PA, 17 3P%, 18 FTM, 19 FTA, 20 FT%, 21 ORB, 22 DRB, 23 TRB, 24 AST, 25 STL, 26 BLK, 27 TOV, 28 PF, 29 PTS, 30 GMSC, 31 +/-
# 4 DATE, 5 AGE, 7 HOME/AWAY, 9 RESULT, 11 MP, 31 +/1

# --------------------------------------------------------------------------------

# 4 DATE, 2015-10-28
# s = '2015-10-28'
# year, month, day = s.split('-')
# print year, month, day

# 5 AGE, 29-049
# s = '29-049'
# years, days = s.split('-')
# make sure to add int(days)
# days = float(years[1])/365.25
# years = float(years[0]) + float(days)

# 7 HOME/AWAY
# s = '@'
# if s == None or s == '' or s == ' ':
# 	print 'home'
# else:
# 	print 'away'

# 9 RESULT, W (+16)
# w = 'W (+16)'
# l = 'L (-14)'

# if 'W' in w and True == False:
# 	w = w[w.find('+') + 1:w.rfind(')')]
# 	print w
# else:
# 	l = l[l.find('-'):l.rfind(')')]
# 	print l

# 11 MP, 21:28
# s = '21:28'
# s = s.split(':')
# s = float(s[0]) + float(s[1])/60

# 31 +/-, -1, 0, 1

# w = '+4'
# l = '-4'
# n = '0'

# if '+' in w and True == False:
# 	w = w[w.find('+'):]
# 	print w
# elif '-' in l and True == False:
# 	l = l[l.find('-'):]
# 	print l
# else:
# 	print n