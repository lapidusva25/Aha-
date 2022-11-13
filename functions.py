import requests
import json


def findAccountID_fromEmail(emailtoFind,token):
  verbose=False

  url = "https://api.totango.com/api/v1/search/users"
  
  payload = 'team_id=-1&query={"terms":[{"type":"string_attribute","attribute":"Email","in_list":["'+emailtoFind+'"]}],"count":1000,"offset":0,"fields":[{"type":"string_attribute","attribute":"Email","field_display_name":"Email"}],"scope":"all"}'
  headers = {
    'app-token': token,
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  count=0
  lstResults = []
  while(count<4):
    try:
      response = requests.request("POST", url, data=payload, headers=headers)
      resp =json.loads(response.text)
      count=4
    except json.decoder.JSONDecodeError:
      if(verbose):
        print('retrying ',count)
      count+=1
  if(verbose):
    print('--------------------received response from Totango with users--------------------')
    print(resp)

  if 'error' in resp:
    return('Error')
  dictResponses = resp['response']['users']['hits']
  for user in dictResponses:
    lstResults.append({'userID':user['name'],'accountID':user['account']['name']})
  return(lstResults)
