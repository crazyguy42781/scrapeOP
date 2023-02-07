############ Final oddsportal scraper

# ATP, baseball, basket, darts, eSports, football, nfl, nhl, rugby
''' Create 4 main functions : scrape_historical, scrape_specific_season, scrape current_season, scrape_next_games
NB : You need to be in the right repository to import functions...'''
import os

# os.chdir("C:\\Users\\Sébastien CARARO\\Desktop\\ATP& &Others\\WebScraping")
from main import scrape_oddsportal_historical


if __name__ == '__main__':
    print('Data will be saved in the following directory:', os.getcwd())

    scrape_oddsportal_historical(sport='soccer', country='france', league='ligue-1', start_season='2003-2004', nseasons=1,
                                 current_season='no', max_page=1)
    # scrape_oddsportal_current_season(sport = 'basketball', country = 'usa', league = veikkausliiga', season = '2020', max_page = 25)
    # scrape_oddsportal_specific_season(sport = 'soccer', country = 'finland', league = 'veikkausliiga', season = '2019', max_page = 25)
    # scrape_oddsportal_next_games(sport = 'tennis', country = 'germany', league = 'exhibition-bett1-aces-berlin-women', season = '2020')


    # Redoing 2003 - 2008 to make sure we get all the games
    # scrape_oddsportal_historical(sport='soccer', country='france', league='ligue-1', start_season='2008-2009', nseasons=1,
    #                              current_season='no', max_page=1)
    # skipping 2009/2010 - already processed
    # 2011 - 2013 were not fully processed. then finishing through 2021
    # scrape_oddsportal_historical(sport='soccer', country='france', league='ligue-1', start_season='2010-2011', nseasons=1,
    #                              current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='japan', league='j1-league', start_season='2004', nseasons=11,
    #                              current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='brazil', league='serie-a', start_season='2019', nseasons=3,
    #                             current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='england', league='championship', start_season='2018-2039',
    #                              nseasons=4, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='england', league='league-one', start_season='2003-2004',
    #                              nseasons=19, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='england', league='league-two', start_season='2003-2004',
    #                              nseasons=19, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='mexico', league='primera-division', start_season='2018-2019',
    #                              nseasons=1, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='mexico', league='liga-mx', start_season='2019-2020',
    #                              nseasons=3, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='sweden', league='allsvenskan', start_season='2008',
    #                              nseasons=14, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='australia', league='a-league', start_season='2021-2022',
    #                              nseasons=1, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='italy', league='serie-a', start_season='2020-2021',
    #                              nseasons=2, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='spain', league='primera-division', start_season='2003-2004',
    #                              nseasons=13, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='spain', league='laliga', start_season='2016-2017',
    #                              nseasons=6, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='england', league='premier-league', start_season='2006-2007',
    #                              nseasons=13, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='usa', league='mls', start_season='2019',
    #                              nseasons=3, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='american-football', country='usa', league='nfl', start_season='2021-2022',
    #                              nseasons=1, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='basketball', country='usa', league='nba', start_season='2020-2021',
    #                              nseasons=2, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='baseball', country='usa', league='mlb', start_season='2016',
    #                              nseasons=15, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='hockey', country='usa', league='nhl', start_season='2005/2006',
    #                              nseasons=17, current_season='no', max_page=1)

    # ------------------------------ second request -------------------------------------------
    # scrape_oddsportal_historical(sport='soccer', country='germany', league='bundesliga', start_season='2003/2004',
    #                              nseasons=19, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='portugal', league='primeira-liga', start_season='2003/2004',
    #                              nseasons=18, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='portugal', league='liga-portugal', start_season='2021/2022',
    #                              nseasons=1, current_season='no', max_page=1)

    # scrape_oddsportal_historical(sport='soccer', country='netherlands', league='eredivisie', start_season='2003/2004',
    #                              nseasons=19, current_season='no', max_page=1)
