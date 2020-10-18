#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from cloudant.client import Cloudant

def accountSetUp(username, password):
    client = Cloudant.iam("d02a0070-4a25-4e81-b712-a8e6c38a8863-bluemix", "0CpvlhxnS58tIZMsdu4QuUqw4bai6t1EYcJAv4Mo4lnI")
    client.connect()
    database_name = "user_db"
    # print(client.all_dbs())
    db = client[database_name] #open database
    print(db)
    userDoc = db["user1"]
    print(userDoc)
    userDoc['username'] = username
    userDoc['password'] = password
    ## make calls to ncr stuff and return back user dictionary
    userDoc['userData'] = {} #replace this later with user object akshay makes
    userDoc.save()



def main(dict):
    accountSetUp(dict['username'], dict['password'])
    return { 'message': 'Hello world' }
