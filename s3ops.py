import pandas as pd
import boto3
from io import StringIO
from inspect import getmembers
import io




def GetS3File(path_filename,key,secret,bucket):

    
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)
    obj = s3.get_object(Bucket=bucket, Key=path_filename)
    
    
    dataframe = pd.read_csv(io.BytesIO(obj['Body'].read()), dtype=str, error_bad_lines = False, encoding='latin1')
    print(dataframe)
    return(dataframe)

def FileOutput(df,path_filename,key,secret,bucket,index):
    #usage:
    #key = OUTPATH +region_name + '_devices(collection(AccountID_CollectionID)).csv'
    #FileOutput(df, key)
    #passed DF should be reindexed.
    s3_resource = boto3.resource('s3', aws_access_key_id=key, aws_secret_access_key=secret)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=index, header=True)
    s3_resource.Object(bucket,path_filename).put(Body=csv_buffer.getvalue())

