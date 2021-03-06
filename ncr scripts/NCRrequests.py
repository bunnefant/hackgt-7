#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import requests
from geopy.geocoders import Nominatim
import googlemaps
from googlemaps import places
import config


class NCRrequests:

    def __init__(self, user):
        self.user = user
        self.transactions = self.getTransactions()
        self.bills = []
        self.account = self.getCheckingAccount()
        self.address = ""
        self.essentials = ""
        self.budget = 0
        self.investments = []

    def getNCRAccessToken(self):
        url = "http://ncrdev-dev.apigee.net/digitalbanking/oauth2/v1/token"

        payload = 'grant_type=client_credentials&scopes=accounts%3Aread%2Ctransactions%3Aread%2Ctransfers%3Awrite%2Caccount%3Awrite%2Cinstitution-users%3Aread%2Crecipients%3Aread%2Crecipients%3Awrite%2Crecipients%3Adelete%2Cdisclosures%3Aread%2Cdisclosures%3Awrite'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic alI3RWg3dUF5cFQ0dEpMb0xVMmRBTVlHQ1l5ejZsVjg6T3FRZXQ0OE5YWDdTQXB4SA==',
            'transactionId': 'd7df6cb8-9ca6-44a4-903e-01dc8cb7f02d',
            'institutionId': '00516',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.json()['access_token'])
        return response.json()['access_token']

    # print(getNCRAccessToken())

    def getAccountsOfUser(self):
        while True:
            url = "http://ncrdev-dev.apigee.net/digitalbanking/db-accounts/v1/accounts?hostUserId=" + self.user
            token = self.getNCRAccessToken()
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + token,
                'transactionId': '1823351b-363d-4c50-9d40-02ef54353ce8',
                'Accept': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            try:
                if response.json()['code'] == "CMN_90000":
                    print('need to make request again')
            except:
                break
        return response.json()

    def getCheckingAccountId(self):
        accounts = self.getAccountsOfUser()['accounts']
        id = None
        for x in accounts:
            if x['type']['value'] == "CHECKING":
                id = x['id']
        return id

    # print(getCheckingAccount("HACKATHONUSER002"))

    def getCheckingAccount(self):
        accounts = self.getAccountsOfUser()['accounts']
        account = None
        for x in accounts:
            if x['type']['value'] == "CHECKING":
                account = x
                break
        finalAccount = {}
        finalAccount['description'] = account['description']
        finalAccount['accountNumber'] = account['accountNumber']
        finalAccount['type'] = 'CHECKING'
        finalAccount['currentBalance'] = float(account['currentBalance']['amount'])
        finalAccount['interestRate'] = float(account['interestRate'])
        return finalAccount

    def getTransactions(self):
        while True:
            url = "http://ncrdev-dev.apigee.net/digitalbanking/db-transactions/v1/transactions?accountId=rf5ao6Qclwsth9OfOvUb-EeV1m2BfmTzUEALGLQ3ehU&hostUserId=" + self.user
            token = self.getNCRAccessToken()
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + token,
                'transactionId': 'fdd1542a-bcfd-439b-a6a1-5a064023b0ce',
                'Accept': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            try:  # keep trying to make request until we dont get an error code
                if response.json()['code'] == "CMN_90000":
                    print('need to make request again')
            except:
                break
        return response.json()

    # print(getTransactions(getCheckingAccount("HACKATHONUSER002")))

    def listPastTransactions(self):
        # implement method to list all transactions cleanly in a listPastTransactions
        # only withdrawls
        # probably transaction number, date, memo, description, amount
        # return list of jsons with just that
        transactionList = self.getTransactions()['transactions']
        finalList = [{'transactionNumber': 0, 'date': '01/01/2020', 'memo': 'Transaction Memo',
                      'description': 'Transaction Description', 'amount': 0}]
        for x in transactionList:
            temp = {}
            temp['transactionNumber'] = int(x['transactionNumber'])
            temp['date'] = x['transactionDate']
            temp['memo'] = x['memo']
            temp['description'] = x['description']
            temp['amount'] = float(x['amount']['amount'])
            finalList.insert(0, temp)
        finalList.pop()
        return finalList

    def returnUserObject(self):
        instance_dict = {"transactions" : self.transactions, "bills" : self.bills, "accountInformation" : self.account,
        "address" : self.address, "essentials" : self.essentials, "budget" : self.budget, "investments" : self.investments}
        return instance_dict

    def addInvestment(self, stock_name, points):
        temp = {'name' : stock_name, 'points' : points}
        self.investments.append(temp)

    def find_closest_foodbank(self, address):
        geolocator = Nominatim(user_agent="foodBankLocator")
        location = geolocator.geocode(address)
        coordinates = (location.latitude, location.longitude)
        client = googlemaps.Client(key=config.googleKey)
        nearby_banks = places.places_nearby(client=client, location=coordinates, radius=24140, keyword='food bank')
        food_bank_list = []
        for foodbank in nearby_banks['results']:
            location_coord = foodbank['geometry']['location']['lat'], foodbank['geometry']['location']['lng']
            address = geolocator.reverse(str(location_coord[0]) + ", " + str(location_coord[1]))
            food_bank_list.append(foodbank['name'])
        print(food_bank_list)
        return food_bank_list


def main(dict):
    ncr_req = NCRrequests("HACKATHONUSER005")
    # data = ncr_req.listPastTransactions()
    # print(data)
    data = ncr_req.returnUserObject()
    print(data)
    ncr_req.find_closest_foodbank("Clough Undergraduate Learning Commons")
    return {'message': data}

#uncoment to test data
main({})
