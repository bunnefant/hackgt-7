import requests

#response = requests.get("https://www.blackrock.com/tools/api-tester/hackathon?apiType=portfolioAnalysis&calculateExpectedReturns=true&calculateExposures=true&calculatePerformance=true&positions=NUS~29.85%7CMMIAX~38.34%7CICAUX~31.82%7C&runJsFunctionEveryTime=true")


portfolio_analysis_request = requests.get("https://www.blackrock.com/tools/hackathon/security-data",
                                          params={'identifiers': "ticker:AAPL,ticker:MSFT,ticker:RKUNY"})

print(portfolio_analysis_request.status_code)
print(portfolio_analysis_request.json())
