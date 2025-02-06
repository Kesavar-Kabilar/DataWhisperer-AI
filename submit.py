import requests
import json
import uuid

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp3-lexv2-autograder"

payload = {
	"graphApi": "https://idf5nik85g.execute-api.us-east-1.amazonaws.com/APIStage", #<post api for storing the graph>
	"botId": "XE7SFD25UU", # <id of your Amazon Lex Bot>
	"botAliasId": "PXKPK48ABV", #<Lex alias id>
	"identityPoolId": "us-east-1:4a752a76-f042-4a9e-b875-ef9736a6ba1a", #<cognito identity pool id for lex>
	"accountId": "418272780523", #<your aws account id used for accessing lex>
	"submitterEmail": "kabilar2@illinois.edu", # <insert your coursera account email>
	"secret": "ZeBzFDTk7dYOFizn", # <insert your secret token from coursera>
	"region": "us-east-1", #<Region where your lex is deployed (Ex: us-east-1)>
    }

r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)