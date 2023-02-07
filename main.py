import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from create_clean_table import *

CWD = os.getcwd()
global DRIVER_LOCATION
DRIVER_LOCATION = "chromedriver.exe"
# you can change to 'OPENING' if you want to collect opening odds,
# any other value will make the program collect CLOSING odds
TYPE_ODDS = 'CLOSING'


def fi(a):
    try:
        # driver.find_element_by_xpath(a).text
        driver.find_element(by=By.XPATH, value=a).text
    except:
        return False
    return True


def ffi(a):
    if fi(a):
        # return driver.find_element_by_xpath(a).text
        return driver.find_element(by=By.XPATH, value=a).text


def ffi9(a):
    c = driver.find_elements(by=By.CLASS_NAME, value=a)
    return len(c)


def num_pages():
    c = driver.find_elements(by=By.XPATH, value=f'//*[@class="w-6 h-6 bg-no-repeat bg-skip-next"]')
    max_pg = ""
    for each in c:
        max_pg = each.get_attribute(':href')
    max_pr_stripped = max_pg.split('page')[1].split('/')[1]

    return max_pr_stripped


def fi2(a):
    try:
        # driver.find_element_by_xpath(a).click()
        driver.find_element(By.XPATH, value=a).click()
    except:
        return False
    return True


def ffi2(a):
    c = driver.find_element(by=By.XPATH, value=a)
    if 'deactivate' in c.get_attribute('class'):
        a += '/td[2]/a'
        driver.find_element(by=By.XPATH, value=a).click()
        return True
    return False


def fffi(a):
    if TYPE_ODDS == 'OPENING':
        try:
            return get_opening_odd(a)
        except:
            return ffi(a)
    else:
        return ffi(a)


def get_opening_odd(xpath):
    # I. Get the raw data by hovering and collecting
    data = driver.find_element(by=By.XPATH, value=xpath)
    hov = ActionChains(driver).move_to_element(data)
    hov.perform()
    data_in_the_bubble = driver.find_element(by=By.XPATH, value="//*[@id='tooltiptext']")
    hover_data = data_in_the_bubble.get_attribute("innerHTML")

    # II. Extract opening odds
    b = re.split('<br>', hover_data)
    c = [re.split('</strong>', y)[0] for y in b][-2]
    opening_odd = re.split('<strong>', c)[1]

    # print(opening_odd)
    return opening_odd


def get_links():
    data = []
#    c = driver.find_elements(by=By.CLASS_NAME, value='deactivate')
    count = 1
    # for each in c:
    #     elements = each.find_element(by=By.XPATH, value='td[2]/a')
    #     len_td = len(each.find_elements(by=By.XPATH, value='td'))
    #     e2 = each.find_element(by=By.XPATH, value=f'td[{len_td}]').text
    #     # print(elements.get_attribute('href'), e2)
    #     data += [(elements.get_attribute('href'), e2, count)]
    #     count += 1
    #driver.close()
    #exit(1)
    c = driver.find_elements(by=By.XPATH, value=f'//*[@class="flex flex-col w-full text-xs"]')
    for each in c:
        elements = each.find_element(by=By.XPATH, value='div/div/a')
        len_div = len(each.find_elements(by=By.XPATH, value='div/div[1]'))
        e2 = each.find_element(by=By.XPATH, value=f'div/div/div[{len_div}]/div').text
        data += [(elements.get_attribute('href'), e2, count)]
        count += 1
    return data


def scrape_oddsportal_historical(sport='football', country='france', league='ligue-1', start_season='2019-2020',
                                 nseasons=1, current_season='yes', max_page=25):
    '''
        sport : sport as mentioned on the oddsportal website
        country : country as mentioned on oddsportal website
        league : league as mentioned on oddsportal website
        start_season : starting season as mentioned in the oddsportal website
        nseasons = number of seasons to scrape from the starting season (do not include current season!)
        current_season : do you want to scrape current season aswell ?
    '''
    L = ['soccer', 'basketball', 'baseball', 'hockey', 'tennis', 'american-football', 'aussie-rules', 'badminton',
         'bandy', 'beach-volleyball', 'boxing', 'cricket', 'darts', 'esports', 'floorball', 'futsal', 'handball',
         'mma', 'rugby-league', 'rugby-union', 'tabel-tennis', 'volleyball', 'water-polo']

    while sport not in L:
        sport = input('Please choose a sport among the following list : \n {} \n'.format(L))

    if sport == 'tennis':
        bestof = input('Please indicate the format of tournament (3 sets or 5 sets) : \n ')
        surface = input('Please indicate the surface : \n ')

    if not os.path.exists(CWD + f'/{sport}'):
        os.makedirs(CWD + f'/{sport}')

    if sport in ['baseball', 'esports', 'basketball', 'darts', 'american-football', 'volleyball']:
        df = scrape_league_typeA(Season=start_season, sport=sport, country1=country, tournament1=league,
                                 nseason=nseasons, current_season=current_season, max_page=max_page)
        df = create_clean_table_two_ways(df)
    # elif sport in ['tennis']:
    # df = scrape_league_typeB(Surface = surface, bestof = bestof, Season = start_season, country1 = country, tournament1 = league, nseason = nseasons)
    # df = create_clean_table_two_ways(df)
    elif sport in ['soccer', 'rugby-union', 'rugby-league', 'handball']:
        df = scrape_league_typeC(Season=start_season, sport=sport, country1=country, tournament1=league,
                                 nseason=nseasons, current_season=current_season, max_page=max_page)
        df = create_clean_table_three_ways(df)
    elif sport in ['hockey']:
        df = scrape_league_typeD(Season=start_season, sport=sport, country1=country, tournament1=league,
                                 nseason=nseasons, current_season=current_season, max_page=max_page)
        df = create_clean_table_two_ways(df)

    df.to_csv(CWD + f'/{sport}/Historical_{country}_{league}.csv', sep=',', encoding='utf-8', index=False)


def scrape_league_typeC(Season, sport, country1, tournament1, nseason, current_season='yes', max_page=25):
    # indicates whether Season is in format '2010-2011' or '2011' depends on the league)
    global driver
    driver = webdriver.Chrome(executable_path=DRIVER_LOCATION)
    long_season = (len(Season) > 6)
    Season = int(Season[0:4])
    for i in range(nseason):
        SEASON1 = f'{Season}'
        if long_season:
            SEASON1 = f'{Season}-{Season + 1}'
        print(f'We start to collect season {SEASON1}')
        scrape_current_tournament_typeC(sport=sport, tournament=tournament1, country=country1, SEASON=SEASON1,
                                        max_page=max_page)
        print(f'We finished to collect season {SEASON1} !')
        Season += 1
    driver.close()
    # Finally we merge all files

    file1 = pd.read_csv(CWD + f'/{sport}/{country1}/{tournament1}/' + os.listdir(CWD + f'/{sport}/{country1}/{tournament1}/')[0], sep=';')
    print(os.listdir(CWD + f'/{sport}/{country1}/{tournament1}/')[0])
    for filename in os.listdir(CWD + f'/{sport}/{country1}/{tournament1}/')[1:]:
        file = pd.read_csv(CWD + f'/{sport}/{country1}/{tournament1}/' + filename, sep=';')
        print(filename)
        # file1 = file1.append(file)
        file1 = pd.concat([file1, file], ignore_index=True, sort=False)
    file1 = file1.reset_index()

    # Correct falsely collected data for away (in case of 1X2 instead of H/A odds)
    return file1


def scrape_current_tournament_typeC(sport, tournament, country, SEASON, max_page=25):
    global driver
    ############### NOW WE SEEK TO SCRAPE THE ODDS AND MATCH INFO################################
    DATA_ALL = []
    link = f'https://www.oddsportal.com/{sport}/{country}/{tournament}-{SEASON}/results/#/page/1'
    driver.get(link)
    num_p = int(num_pages())
    if max_page == 0:
        print('You have selected to get all pages')
        max_pg = num_p
    elif num_p <= max_page:
        print('You have entered more page numbers than there currently are.')
        print('Setting max pages to current number of pages')
        max_pg = num_p
    else:
        print('You have entered less pages than there currently is.')
        print('Setting max pages to the entered value.')
        max_pg = max_page

    for page in range(1, max_pg + 1):
        print(f'We start to scrape the page n°{page} of {max_pg}')
        data = scrape_page_typeC(page, sport, country, tournament, SEASON)

        DATA_ALL = DATA_ALL + [y for y in data if y is not None]

    data_df = pd.DataFrame(DATA_ALL)

    try:
        data_df.columns = ['TeamsRaw', 'Bookmaker', 'OddHome', 'OddDraw', 'OddAway', 'DateRaw', 'ScoreRaw']
    except:
        print('Function crashed, probable reason : no games scraped (empty season)')
        return 1
    ##################### FINALLY WE CLEAN THE DATA AND SAVE IT ##########################
    '''Now we simply need to split team names, transform date, split score'''

    # (0) Filter out None rows
    data_df = data_df[~data_df['Bookmaker'].isnull()].dropna().reset_index()
    data_df["TO_KEEP"] = 1
    for i in range(len(data_df["TO_KEEP"])):
        if len(re.split(':', data_df["ScoreRaw"][i])) < 2:
            data_df["TO_KEEP"].iloc[i] = 0

    data_df = data_df[data_df["TO_KEEP"] == 1]

    # (a) Split team names
    data_df["Home_id"] = [re.split(' - ', y)[0] for y in data_df["TeamsRaw"]]
    data_df["Away_id"] = [re.split(' - ', y)[1] for y in data_df["TeamsRaw"]]
    # (b) Transform date
    data_df["Date"] = [re.split(', ', y)[1] for y in data_df["DateRaw"]]
    # (c) Split score
    data_df["Score_home"] = [re.split(':', y)[0][-2:] for y in data_df["ScoreRaw"]]
    data_df["Score_away"] = [re.split(':', y)[1][:2] for y in data_df["ScoreRaw"]]
    # (e) Set season column
    data_df["Season"] = SEASON
    # Finally we save results
    if not os.path.exists(CWD + f'/{sport}/{country}/{tournament}_FULL'):
        os.makedirs(CWD + f'/{sport}/{country}/{tournament}_FULL')
    if not os.path.exists(CWD + f'/{sport}/{country}/{tournament}'):
        os.makedirs(CWD + f'/{sport}/{country}/{tournament}')

    data_df.to_csv(CWD + f'/{sport}/{country}/{tournament}_FULL/{tournament}_{SEASON}_FULL.csv', sep=';', encoding='utf-8',
                   index=False)
    data_df[['Home_id', 'Away_id', 'Bookmaker', 'OddHome', 'OddDraw', 'OddAway', 'Date', 'Score_home', 'Score_away',
             'Season']].to_csv(CWD + f'/{sport}/{country}/{tournament}/{tournament}_{SEASON}.csv', sep=';', encoding='utf-8',
                               index=False)

    return data_df


def scrape_page_typeC(page, sport, country, tournament, SEASON):
    # for p in range(1, num_p + 1):
    time.sleep(1)
    link = f'https://www.oddsportal.com/{sport}/{country}/{tournament}-{SEASON}/results/#/page/{page}'
    driver.get(link)
    time.sleep(3)
    # n_count = ffi9('deactivate')
    links = get_links()
    return get_data_typeC(links)


def get_data_typeC(links):
    DATA = []
    for each in links:
        # print('We wait 2 seconds')
        print(f'Working on match {each[2]} of {len(links)}')
        L = []
        time.sleep(2)
        driver.get(each[0])
        #time.sleep(2)
        # Now we collect all bookmaker
        c = driver.find_elements(by=By.XPATH, value=f'//*[@class="flex text-xs max-sm:h-[60px] h-9 border-b"]')
        final_score = driver.find_element(by=By.XPATH, value=f'//*[@class="flex max-sm:gap-2 max-sm:!mb-5"]/div[2]/strong').text
        date = driver.find_element(by=By.XPATH, value=f'//*[@class="flex text-xs font-normal text-gray-dark font-main item-center"]/div[2]').text.split(",")[1]
        match = driver.find_element(by=By.XPATH, value=f'//*[@class="capitalize font-normal text-[0.70rem] leading-4 max-mt:!hidden"]/p').text
        check = driver.find_elements(by=By.XPATH, value=f'//*[@class="flex h-8 border-b border-l bg-gray-med_light"]/div')
        for e in c:
            Book = e.find_element(by=By.XPATH, value='div/a/p').text
            Odd_1 = e.find_element(by=By.XPATH, value=f'div[{2}]/div/p').text
            if len(check) == 4:
                Odd_2 = e.find_element(by=By.XPATH, value=f'div[{3}]/div/p').text
                L = L + [(match, Book, Odd_1, Odd_2, date, final_score)]
            else:
                Odd_X = e.find_element(by=By.XPATH, value=f'div[{3}]/div/p').text if len(check) == 5 else None
                Odd_2 = e.find_element(by=By.XPATH, value=f'div[{4}]/div/p').text
                L = L + [(match, Book, Odd_1, Odd_X, Odd_2, date, final_score)]
            print(match, Book, Odd_1, Odd_X, Odd_2, date, final_score)
        DATA += L
    print(DATA)
    return DATA


# ----------------------------- Type A -------------------------------------------


def get_data_typeA(n_count, links):
    DATA = []
    for each in links:
        print(f'Working on match {each[2]} of {len(links)}. Link {each[0]}')
        L = []
        driver.get(each[0])
        time.sleep(2)
        # Now we collect all bookmaker
        for j in range(1, int(each[1]) + 1):  # only first 10 bookmakers displayed
            Book = ffi(
                f'//*[@id="odds-data-table"]/div[1]/table/tbody/tr[{j}]/td[1]/div/a[2]')  # first bookmaker name
            Odd_1 = fffi(f'//*[@id="odds-data-table"]/div[1]/table/tbody/tr[{j}]/td[2]/div')  # first home odd
            Odd_2 = fffi(f'//*[@id="odds-data-table"]/div[1]/table/tbody/tr[{j}]/td[3]/div')  # first away odd
            match = ffi('//*[@id="col-content"]/h1')  # match teams
            final_score = ffi('//*[@id="event-status"]')
            date = ffi('//*[@id="col-content"]/p[1]')  # Date and time
            # print(match, Book, Odd_1, Odd_2, date, final_score, i, '/ 500 ')
            L = L + [(match, Book, Odd_1, Odd_2, date, final_score)]
        DATA += L
    print(DATA)
    return DATA


def scrape_page_typeA(page, sport, country, tournament, SEASON):
    # for p in range(1, num_p + 1)
    time.sleep(1)
    link = f'https://www.oddsportal.com/{sport}/{country}/{tournament}-{SEASON}/results/#/page/{page}'
    driver.get(link)
    time.sleep(3)
    n_count = ffi9('deactivate')
    links = get_links()
    return get_data_typeA(n_count, links)


def scrape_current_tournament_typeA(sport, tournament, country, SEASON, max_page=25):
    global driver
    ############### NOW WE SEEK TO SCRAPE THE ODDS AND MATCH INFO################################
    DATA_ALL = []
    link = f'https://www.oddsportal.com/{sport}/{country}/{tournament}-{SEASON}/results/#/page/1'
    driver.get(link)
    num_p = int(num_pages())
    for page in range(1, num_p +1):
        print(f'We start to scrape the page n°{page} of {num_p}')
        data = scrape_page_typeA(page, sport, country, tournament, SEASON)
        DATA_ALL = DATA_ALL + [y for y in data if y != None]

    data_df = pd.DataFrame(DATA_ALL)
    try:
        data_df.columns = ['TeamsRaw', 'Bookmaker', 'OddHome', 'OddAway', 'DateRaw', 'ScoreRaw']
    except:
        print('Function crashed, probable reason : no games scraped (empty season)')
        return 1
    ##################### FINALLY WE CLEAN THE DATA AND SAVE IT ##########################
    '''Now we simply need to split team names, transform date, split score'''

    # (0) Filter out None rows
    data_df = data_df[~data_df['Bookmaker'].isnull()].dropna().reset_index()
    data_df["TO_KEEP"] = 1
    for i in range(len(data_df["TO_KEEP"])):
        if len(re.split(':', data_df["ScoreRaw"][i])) < 2:
            data_df["TO_KEEP"].iloc[i] = 0

    data_df = data_df[data_df["TO_KEEP"] == 1]

    # (a) Split team names
    data_df["Home_id"] = [re.split(' - ', y)[0] for y in data_df["TeamsRaw"]]
    data_df["Away_id"] = [re.split(' - ', y)[1] for y in data_df["TeamsRaw"]]
    # (b) Transform date
    data_df["Date"] = [re.split(', ', y)[1] for y in data_df["DateRaw"]]
    # (c) Split score
    data_df["Score_home"] = [re.split(':', y)[0][-3:] for y in data_df["ScoreRaw"]]
    data_df["Score_away"] = [re.split(':', y)[1][:3] for y in data_df["ScoreRaw"]]
    for j in range(len(data_df["Score_home"])):
        str_home = data_df["Score_home"].iloc[j]
        str_away = data_df["Score_away"].iloc[j]
        if str_home[0] == 't':
            data_df["Score_home"].iloc[j] = str_home[1:]
        if str_away[-1] == '(':
            data_df["Score_away"].iloc[j] = str_away[:-1]
    # (e) Set season column
    data_df["Season"] = SEASON
    # Finally we save results
    file_path = CWD + f'/{sport}/{country}/{tournament}'
    if not os.path.exists(file_path + '_FULL'):
        os.makedirs(file_path + '_FULL')
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    data_df.to_csv(file_path + f'_FULL/{tournament}_{SEASON}_FULL.csv', sep=';', encoding='utf-8', index=False)
    data_df[
        ['Home_id', 'Away_id', 'Bookmaker', 'OddHome', 'OddAway', 'Date', 'Score_home', 'Score_away', 'Season']].to_csv(
        file_path + f'/{tournament}_{SEASON}.csv', sep=';', encoding='utf-8', index=False)

    return data_df


def scrape_league_typeA(Season, sport, country1, tournament1, nseason, current_season='yes', max_page=25):
    # indicates whether Season is in format '2010-2011' or '2011' depends on the league)
    global driver
    driver = webdriver.Chrome(executable_path=DRIVER_LOCATION)
    long_season = (len(Season) > 6)
    Season = int(Season[0:4])
    for i in range(1, nseason + 1):
        SEASON1 = '{}'.format(Season)
        if long_season:
            SEASON1 = '{}-{}'.format(Season, Season + 1)
        print(f'We start to collect season {SEASON1}')
        scrape_current_tournament_typeA(sport=sport, tournament=tournament1, country=country1, SEASON=SEASON1,
                                        max_page=max_page)
        print('We finished to collect season {} !'.format(SEASON1))
        Season += 1
    driver.close()

    # Finally we merge all files
    file_path = CWD + f'/{sport}/{country1}/{tournament1}/'
    file1 = pd.read_csv(file_path + os.listdir(file_path)[0], sep=';')
    print(os.listdir(file_path)[0])
    for filename in os.listdir(file_path)[1:]:
        file = pd.read_csv(file_path + filename, sep=';')
        print(filename)
        file1 = pd.concat([file1, file], ignore_index=True, sort=False)
    file1 = file1.reset_index()

    # Correct falsly collected data for away (in case of 1X2 instead of H/A odds)
    for i in range(file1.shape[0]):
        if (1 / file1["OddHome"].iloc[i] + 1 / file1["OddAway"].iloc[i]) < 1:
            file1["OddAway"].iloc[i] = 1 / (
                    (1 - 1 / file1["OddHome"].iloc[i]) * 1.07)  # 1/1.07 = 0.934 => 6.5 % margin (estimation)
            print(file1["OddHome"].iloc[i], file1["OddAway"].iloc[i], i)
    #file1.to_csv("./{}/All_data_{}.csv".format(tournament1, tournament1))

    print('All good! ')
    return file1

# ----------------------------- Type D -------------------------------------------

def scrape_league_typeD(Season, sport, country1, tournament1, nseason, current_season='yes', max_page=25):
    # indicates whether Season is in format '2010-2011' or '2011' depends on the league)
    global driver
    driver = webdriver.Chrome(executable_path=DRIVER_LOCATION)
    long_season = (len(Season) > 6)
    Season = int(Season[0:4])
    for i in range(nseason):
        SEASON1 = f'{Season}'
        if long_season:
            SEASON1 = f'{Season}-{Season + 1}'
        print(f'We start to collect season {SEASON1}')
        scrape_current_tournament_typeD(sport=sport, tournament=tournament1, country=country1, SEASON=SEASON1,
                                        max_page=max_page)
        print(f'We finished to collect season {SEASON1} !')
        Season += 1
    driver.close()

    # Finally we merge all files
    file_path = CWD + f'/{sport}/{country1}/{tournament1}/'
    file1 = pd.read_csv(file_path + os.listdir(file_path)[0], sep=';')
    print(os.listdir(file_path)[0])
    for filename in os.listdir(file_path)[1:]:
        file = pd.read_csv(file_path + filename, sep=';')
        print(filename)
        file1 = pd.concat([file1, file], ignore_index=True, sort=False)
    file1 = file1.reset_index()

    # Correct falsly collected data for away (in case of 1X2 instead of H/A odds)
    for i in range(file1.shape[0]):
        if (1 / file1["OddHome"].iloc[i] + 1 / file1["OddAway"].iloc[i]) < 1:
            file1["OddAway"].iloc[i] = 1 / (
                    (1 - 1 / file1["OddHome"].iloc[i]) * 1.07)  # 1/1.07 = 0.934 => 6.5 % margin (estimation)
            print(file1["OddHome"].iloc[i], file1["OddAway"].iloc[i], i)
    #file1.to_csv("./{}/All_data_{}.csv".format(tournament1, tournament1))

    print('All good! ')
    return (file1)


def scrape_current_tournament_typeD(sport, tournament, country, SEASON, max_page=25):
    global driver

    DATA_ALL = []
    link = f'https://www.oddsportal.com/{sport}/{country}/{tournament}-{SEASON}/results/#/page/1'
    driver.get(link)
    num_p = int(num_pages())

    for page in range(1, num_p + 1):
        print(f'We start to scrape the page n°{page} of {num_p}')
        data = scrape_page_typeD(page, sport, country, tournament, SEASON)
        DATA_ALL = DATA_ALL + [y for y in data if y != None]

    data_df = pd.DataFrame(DATA_ALL)
    try:
        data_df.columns = ['TeamsRaw', 'Bookmaker', 'OddHome', 'OddAway', 'DateRaw', 'ScoreRaw']
    except:
        print('Function crashed, probable reason : no games scraped (empty season)')
        return 1
    ##################### FINALLY WE CLEAN THE DATA AND SAVE IT ##########################
    '''Now we simply need to split team names, transform date, split score'''

    # (0) Filter out None rows
    data_df = data_df[~data_df['Bookmaker'].isnull()].dropna().reset_index()
    data_df["TO_KEEP"] = 1
    for i in range(len(data_df["TO_KEEP"])):
        if len(re.split(':', data_df["ScoreRaw"][i])) < 2:
            data_df["TO_KEEP"].iloc[i] = 0

    data_df = data_df[data_df["TO_KEEP"] == 1]
    # (a) Split team names
    data_df["Home_id"] = [re.split(' - ', y)[0] for y in data_df["TeamsRaw"]]
    data_df["Away_id"] = [re.split(' - ', y)[1] for y in data_df["TeamsRaw"]]
    # (b) Transform date
    data_df["Date"] = [re.split(', ', y)[1] for y in data_df["DateRaw"]]
    # (c) Split score
    data_df["Score_home"] = [re.split(':', y)[0][-1:] for y in data_df["ScoreRaw"]]
    data_df["Score_away"] = [re.split(':', y)[1][:1] for y in data_df["ScoreRaw"]]
    # (e) Set season column
    data_df["Season"] = SEASON
    # Finally we save results
    if not os.path.exists(CWD + f'/{sport}/{country}/{tournament}_FULL'):
        os.makedirs(CWD + f'/{sport}/{country}/{tournament}_FULL')
    if not os.path.exists(CWD + f'/{sport}/{country}/{tournament}'):
        os.makedirs(CWD + f'/{sport}/{country}/{tournament}')

    data_df[['Home_id', 'Away_id', 'Bookmaker', 'OddHome', 'OddAway', 'Date', 'Score_home', 'Score_away', 'Season']]. \
        to_csv(CWD + f'/{sport}/{country}/{tournament}/{tournament}_{SEASON}.csv', sep=';', encoding='utf-8', index=False)
    data_df.to_csv(CWD + f'/{sport}/{country}/{tournament}_FULL/{tournament}_{SEASON}_FULL.csv', sep=';', encoding='utf-8',
                   index=False)
    return data_df


def scrape_page_typeD(page, sport, country, tournament, SEASON):
    time.sleep(1)
    link = f'https://www.oddsportal.com/{sport}/{country}/{tournament}-{SEASON}/results/page/1/#/page/{page}'
    driver.get(link)
    time.sleep(3)
    n_count = ffi9('deactivate')
    links = get_links()
    return get_data_typeD(n_count, links)


def get_data_typeD(n_count, links):
    DATA = []
    # target = '//*[@id="tournamentTable"]/tbody/tr[{}]/td[2]/a'.format(i)
    for each in links:
        print(f'Working on match {each[2]} of {len(links)}. Link {each[0]}')
        L = []
        driver.get(each[0])
        time.sleep(2)
        for j in range(1, int(each[1]) + 1):
            Book = ffi(f'//*[@id="odds-data-table"]/div[1]/table/tbody/tr[{j}]/td[1]/div/a[2]')  # first bookmaker name
            Odd_1 = fffi(f'//*[@id="odds-data-table"]/div[1]/table/tbody/tr[{j}]/td[2]')  # first home odd
            Odd_2 = fffi(f'//*[@id="odds-data-table"]/div[1]/table/tbody/tr[{j}]/td[3]')  # first away odd
            match = ffi('//*[@id="col-content"]/h1')  # match teams
            final_score = ffi('//*[@id="event-status"]')
            date = ffi('//*[@id="col-content"]/p[1]')  # Date and time
            #print(match, Book, Odd_1, Odd_2, date, final_score, i, '/ 500 ')
            L = L + [(match, Book, Odd_1, Odd_2, date, final_score)]
        DATA += L
    return DATA





