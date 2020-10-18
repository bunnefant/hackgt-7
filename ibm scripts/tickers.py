from cloudant.client import Cloudant
def saveTickers(tickers):
    client = Cloudant.iam("d02a0070-4a25-4e81-b712-a8e6c38a8863-bluemix", "0CpvlhxnS58tIZMsdu4QuUqw4bai6t1EYcJAv4Mo4lnI")
    client.connect()
    database_name = "user_db"
    # print(client.all_dbs())
    db = client[database_name] #open database
    print(db)
    userDoc = db["user1"]
    userDoc['tickers'] = tickers
    userDoc.save()

saveTickers(['SRNE', 'SPY'])
