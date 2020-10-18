import sys
import requests
from cloudant.client import Cloudant



def getUserAddress():
    client = Cloudant.iam("d02a0070-4a25-4e81-b712-a8e6c38a8863-bluemix", "0CpvlhxnS58tIZMsdu4QuUqw4bai6t1EYcJAv4Mo4lnI")
    client.connect()
    database_name = "user_db"
    # print(client.all_dbs())
    db = client[database_name] #open database
    print(db)
    userDoc = db["user1"]
    print(userDoc)
    return userDoc['userData']['address']


def getBankInfo():
    client = Cloudant.iam("d02a0070-4a25-4e81-b712-a8e6c38a8863-bluemix", "0CpvlhxnS58tIZMsdu4QuUqw4bai6t1EYcJAv4Mo4lnI")
    client.connect()
    database_name = "user_db"
    # print(client.all_dbs())
    db = client[database_name] #open database
    # print(db)
    userDoc = db["user1"]
    return userDoc['userData']['accountInformation']

def getFoodBanks():
    client = Cloudant.iam("d02a0070-4a25-4e81-b712-a8e6c38a8863-bluemix", "0CpvlhxnS58tIZMsdu4QuUqw4bai6t1EYcJAv4Mo4lnI")
    client.connect()
    database_name = "user_db"
    # print(client.all_dbs())
    db = client[database_name] #open database
    # print(db)
    userDoc = db["user1"]
    return userDoc['foodBanks']

def getUser():
    client = Cloudant.iam("d02a0070-4a25-4e81-b712-a8e6c38a8863-bluemix", "0CpvlhxnS58tIZMsdu4QuUqw4bai6t1EYcJAv4Mo4lnI")
    client.connect()
    database_name = "user_db"
    # print(client.all_dbs())
    db = client[database_name] #open database
    # print(db)
    userDoc = db["user1"]
    return userDoc

def main(dict):
    if dict['type'] == 'investment':
        ## do stuff with rohits code
        print('hello')
    elif dict['type'] == 'food_bank':
        list = getFoodBanks()
        output = "The food banks nearby your address are: \n"
        i = 0
        for x in list:
            if i > 5:
                break
            i += 1
            output += x + "\n"
        output += "Look up the names on Google to find their addresses"
        return {'message' : output}
    elif dict['type'] == 'bank_info':
        info = getBankInfo()
        output = "Here is your account information. This is a " + info['type'] + " account. The name of the account is " + info['description'] + ". Your account number is " + str(info['accountNumber']) + ". Your current balance is " + str(info['currentBalance']) + ". The interest rate you recieve for this account is " + str(info['interestRate']) + "."
        return {'message' : output}
    elif dict['type'] == 'billing':
        return {'message' : getUser()['userData']['bills']}
    elif dict['type'] == 'budget':
        return {'message' : getUser()['userData']['budget']}
    elif dict['type'] == 'transactions':
        ##do stuff with budget, return, change ...
        return {'message' : getUser()['userData']['transactions']}
    elif dict['type'] == 'account_number':
        ##do stuff with budget, return, change ...
        return {'message' : getBankInfo()['accountNumber']}
    elif dict['type'] == 'interest_rate':
        ##do stuff with budget, return, change ...
        return {'message' : getBankInfo()['interestRate']}
    elif dict['type'] == 'account_name':
        ##do stuff with budget, return, change ...
        return {'message' : getBankInfo()['description']}
    elif dict['type'] == 'current_balance':
        ##do stuff with budget, return, change ...
        print(getBankInfo()['currentBalance'])
        return {'message' : getBankInfo()['currentBalance']}
# main({'type' : 'food_bank'})
