import json
import requests
import pandas as pd
from functions import findAccountID_fromEmail
from s3ops import FileOutput,GetS3File
from datetime import datetime,timedelta

totango_token='<your totango token>'
aha_token='<your aha token>'
AWS_key='<your AWS key>'
AWS_secret='<your AWS secret>'
AWS_bucket='<your AWS bucket>'
AWS_path='aha_collection/' #hange to whatever folder make sure it ends with /



def lambda_handler(var1,var2):
	current_date = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')

	df_wishlist = pd.DataFrame(columns=['ahaIDrefID','ahaID','Subject','updated_at','created_at','workflow name','workflow status','body','url','email','accountID','collectionID'])
	df_wishlist = df_wishlist.astype(str)
	
	print(dfPreviousPull)

	dfPreviousPull = pd.DataFrame()
	try:
		dfPreviousPull = GetS3File(AWS_path + 'aha_wishlist_collection_and_timeline.csv',AWS_key,AWS_secret,AWS_bucket).copy(deep=True)
		previousfile = True
	except:
		previousfile = False
	headers = {
		'Authorization': "Bearer " + aha_token,
		'Content-Type': "application/json",
		'Accept': "application/json"
		}

	total_pages = 999
	current_page = 1
	
	while total_pages >= current_page:
		url="https://totango.aha.io/api/v1/ideas?page=" + str(current_page)
		print('previous file boolean',previousfile)
		if(previousfile):
			url= url + "&updated_since="+dfPreviousPull['updated_at'].max()
		print(url)
		print('current:',current_page )
		print('total:',total_pages )
		current_page += 1
		response = requests.request("GET", url, headers=headers)
		resp = json.loads(response.text)
		jsonString=json.dumps(resp['pagination'])
		jsonString=json.loads(jsonString)
		total_pages = (jsonString['total_pages'])

		jsonString=json.dumps(resp['ideas'])
		jsonString=json.loads(jsonString)
		for idea in jsonString:
			
			linetoadd = [idea['reference_num']]
			linetoadd.append(idea['id'])
			linetoadd.append(idea['name'])
			linetoadd.append(idea['updated_at'])
			linetoadd.append(idea['created_at'])
			linetoadd.append(idea['workflow_status']['name'])
			linetoadd.append(idea['workflow_status']['complete'])
			linetoadd.append('Wishlist status: ' + idea['workflow_status']['name'] + '\n\nDescription: ' + idea['description']['body'])
			linetoadd.append(idea['url'])
			url = "https://totango.aha.io/api/v1/ideas/"+idea['reference_num']
			response = requests.request("GET", url, headers=headers)
			resp = json.loads(response.text)
			
			try:
				jsonString=json.dumps(resp['idea']['created_by_idea_user'])
			except KeyError:
				jsonString=json.dumps(resp['idea']['created_by_user'])

			jsonString=json.loads(jsonString)
			linetoadd.append(jsonString['email'])

			for account in findAccountID_fromEmail(jsonString['email'],totango_token):
				linetoadd_copy = linetoadd.copy()
				linetoadd_copy.append(account['accountID'])
				linetoadd_copy.append(account['accountID'] + '-' + idea['id'])
				df_wishlist.loc[len(df_wishlist.index)] = linetoadd_copy

	FileOutput(df= df_wishlist,path_filename = AWS_path + 'aha_wishlist_collection_and_timeline.csv',bucket=AWS_bucket,index=False, key=AWS_key, secret=AWS_secret)

