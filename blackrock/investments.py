import requests
import json
import numpy as np
import math
import time as t
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def getAdvice(keyword, rows, time, risk):
    beginning = t.perf_counter()
    search_url = "https://www.blackrock.com/tools/hackathon/search-securities"
    parameters = {
        'query': keyword,
        'rows': rows
    }

    invests = requests.get(search_url, params=parameters)
    # debug statement
    if invests.status_code == 200:
        print('Call to search is successful')

    data = invests.json()

    tickers = []
    x = 0
    for n in range(0, rows):
        try:
            # get relevant info from data
            avail = data['resultMap']['SEARCH_RESULTS'][0]['resultList'][n]['availability']
            ticker = data['resultMap']['SEARCH_RESULTS'][0]['resultList'][n]['ticker']
            country = data['resultMap']['SEARCH_RESULTS'][0]['resultList'][n]['countryCode']
            score = data['resultMap']['SEARCH_RESULTS'][0]['resultList'][n]['score']

            # dont allow duplicates
            if tickers.count(ticker) < 1 and country == 'US' and avail == 'public':
                tickers.append(ticker)
                # debug
                # print(f'{ticker}  is {avail} in {country} and has score {score}')

        # happens when one of the keys above is not found
        except KeyError:
            # print('ripperoni')
            continue

    print(str(len(tickers)) +
          f'  possible investments for {keyword} were found')

    # get data for each possible investment
    performanceData_url = "https://www.blackrock.com/tools/hackathon/performance"

    ticker_list = ','.join(tickers)

    parameters = {
        'identifiers': ticker_list
    }

    performance = requests.get(performanceData_url, params=parameters)
    # debug statement
    if performance.status_code == 200:
        print('Call to performance is successful')

    data = performance.json()

    # get risk and sharpe ratio for the right time

    # set years that we wanna invest for
    temp_years = 1 if time == 1 else 3 if time == 2 else 5

    # debug stuff
    # print(ticker_list)

    # get the data we need
    stats = np.zeros((len(tickers), 2))
    for n in range(0, len(tickers)):
        # calculate how many years of data we have
        calc_years = 2020 - \
            int(str(data['resultMap']['RETURNS'][n]['startDate'])[:4])
        # years we want to check data for
        years = min(math.floor((time/3) * calc_years) + 1, temp_years)
        if years == 1:
            years = 'one'
        elif years == 2:
            years = 'two'
        elif years == 3:
            years = 'three'
        elif years == 4:
            years = 'four'
        elif years == 5:
            years = 'five'
        try:
            # year risk
            stats[n][0] = data['resultMap']['RETURNS'][n][
                'latestPerf'][f'{years}YearSharpeRatio']
            # year sharp ratio
            stats[n][1] = data['resultMap']['RETURNS'][n]['latestPerf'][f'{years}YearRisk']
        except KeyError:
            stats[n][0] = -9999999
            stats[n][1] = -9999999

    # print(stats)

    # calculate best one

    # pick best investments
    # REMEMBER TO FLIP THIS SHIT OR YOUR WHOLE CODE WILL BE WRONG
    value = stats[:, 0] - (risk * stats[:, 1])
    best_tickers = []
    # get top three choices
    for i in range(0, 3):
        best_ind = np.argmax(value)
        print(
            f'best option is {tickers[best_ind]} with {stats[best_ind][0]} sharp and {stats[best_ind][1]} risk')
        best_tickers.append(tickers.pop(best_ind))
        value = np.delete(value, best_ind)

    print(best_tickers)
    print(t.perf_counter() - beginning)
    return(best_tickers)


def analyzeTicker(tickers):
    beginning = t.perf_counter()
    # get data for each possible investment
    performanceData_url = "https://www.blackrock.com/tools/hackathon/performance"

    ticker_list = ','.join(tickers)

    parameters = {
        'identifiers': ticker_list
    }

    performance = requests.get(performanceData_url, params=parameters)
    # debug statement
    if performance.status_code == 200:
        print('Call to performance is successful')

    data = performance.json()

    temp = ['20201012']
    x = dt.datetime.strptime(temp[0], '%Y%m%d').date().strftime('%b %Y')
    print(x)
    json1 = 0
    json2 = 0
    json3 = 0
    for n in range(0, len(tickers)):
        x = []
        y = []
        for key in data['resultMap']['RETURNS'][n]['returnsMap']:
            x.append(dt.datetime.strptime(
                key, '%Y%m%d').date().strftime('%b %Y'))
            y.append(data['resultMap']['RETURNS'][n]
                     ['returnsMap'][key]['level'])
        if n == 0:
            json1 = {'x': x, 'y': y}
        if n == 1:
            json2 = {'x': x, 'y': y}
        if n == 2:
            json3 = {'x': x, 'y': y}

    # print(len(x))
    # print(x[0])
    # print(len(y))
    # print(y[0])

    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=365))
    # plt.plot(x, y)
    # plt.gcf().autofmt_xdate()
    # plt.ylabel('Level')
    # plt.title(f'{tickers[n]} Level Chart')
    # plt.savefig(f'{tickers[n]}.png')
    # plt.clf()
    # plt.show()

    print('It took ' + str(t.perf_counter() - beginning) + ' seconds.')
    json1 = json.dumps(json1)
    json2 = json.dumps(json2)
    json3 = json.dumps(json3)
    return json1, json2, json3


#dd = getAdvice('sports', 100, 1, 1)
analyzeTicker(['EHC', 'EVDY', 'AAPL'])
