import requests
import json


def getAdvice(keyword, rows):
    search_url = "https://www.blackrock.com/tools/hackathon/search-securities"
    parameters = {
        'query': keyword,
        'rows': rows
    }

    invests = requests.get(search_url, params=parameters)
    # debug statement
    if invests.status_code == 200:
        print('Call successful')

    data = invests.json()

    tickers = []
    x = 0
    for n in range(0, rows):
        try:
            avail = data['resultMap']['SEARCH_RESULTS'][0]['resultList'][n]['availability']

            ticker = data['resultMap']['SEARCH_RESULTS'][0]['resultList'][n]['ticker']

            country = data['resultMap']['SEARCH_RESULTS'][0]['resultList'][n]['countryCode']

            # dont allow duplicates
            if tickers.count(ticker) < 1 and country == 'US' and avail == 'public':
                tickers.append(ticker)
                print(f'{ticker}  is {avail} in {country}')

        except KeyError:
            # print('ripperoni')
            continue


getAdvice('tech', 500)

#
# print(portfolio_analysis_request.json())
