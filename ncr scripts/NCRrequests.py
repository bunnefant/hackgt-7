import requests

def getNCRAccessToken():
    url = "http://ncrdev-dev.apigee.net/digitalbanking/oauth2/v1/token"

    payload = 'grant_type=client_credentials&scopes=accounts%3Aread%2Ctransactions%3Aread%2Ctransfers%3Awrite%2Caccount%3Awrite%2Cinstitution-users%3Aread%2Crecipients%3Aread%2Crecipients%3Awrite%2Crecipients%3Adelete%2Cdisclosures%3Aread%2Cdisclosures%3Awrite'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic alI3RWg3dUF5cFQ0dEpMb0xVMmRBTVlHQ1l5ejZsVjg6T3FRZXQ0OE5YWDdTQXB4SA==',
      'transactionId': 'd7df6cb8-9ca6-44a4-903e-01dc8cb7f02d',
      'institutionId': '00516',
      'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    # print(response.json()['access_token'])
    return response.json()['access_token']
# print(getNCRAccessToken())


def getAccountsOfUser(user):
    while True:
        url = "http://ncrdev-dev.apigee.net/digitalbanking/db-accounts/v1/accounts?hostUserId=" + user
        token = getNCRAccessToken()
        payload = {}
        headers = {
          'Authorization': 'Bearer ' + token,
          'transactionId': '1823351b-363d-4c50-9d40-02ef54353ce8',
          'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data = payload)
        try:
            if response.json()['code'] == "CMN_90000":
                print('need to make request again')
        except:
            break
    return response.json()

# print(getAccountsOfUser("HACKATHONUSER003"))
def getCheckingAccount(user):
    accounts = getAccountsOfUser(user)['accounts']
    id = None
    for x in accounts:
        if x['type']['value'] == "CHECKING":
            id = x['id']
    return id

# print(getCheckingAccount("HACKATHONUSER002"))


def getTransactions(accountID):
    while True:
        url = "http://ncrdev-dev.apigee.net/digitalbanking/db-transactions/v1/transactions?accountId=rf5ao6Qclwsth9OfOvUb-EeV1m2BfmTzUEALGLQ3ehU&hostUserId=HACKATHONUSER100"
        token = getNCRAccessToken()
        payload = {}
        headers = {
          'Authorization': 'Bearer ' + token,
          'transactionId': 'fdd1542a-bcfd-439b-a6a1-5a064023b0ce',
          'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data = payload)
        try:
            if response.json()['code'] == "CMN_90000":
                print('need to make request again')
        except:
            break
    return response.json()


print(getTransactions(getCheckingAccount("HACKATHONUSER002")))

def listPastTransactions():
    #implement method to list all transactions cleanly in a listPastTransactions
    #only withdrawls
    # probably transaction number, date, memo, description, amount
    #return list of jsons with just that
