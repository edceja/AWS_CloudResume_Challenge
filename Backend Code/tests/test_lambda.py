import json
import boto3
import pytest
import moto
from moto import mock_aws

#Make for testing 
@mock_aws
def test_make_table(): 
    dynamodb_mocked =  boto3.resource('dynamodb',region_name="us-west-1").create_table(
        TableName = 'Website_Hits',
        KeySchema = [
                {
                    'AttributeName': 'count_id',
                    'KeyType': 'HASH'
                }
            ],
        AttributeDefinitions = [
                {
                    'AttributeName': 'count_id',
                    'AttributeType': 'S'
                }
            ],
        BillingMode = 'PAY_PER_REQUEST'
        )
        
    dynamodb_mocked.put_item(
        Item={
            'count_id':'site_hits', 'total_views':1
            }
        )

#test adding value to table 
@pytest.fixture    
def test_lambda_handler(event, context):
    #Get the service resource.
    
    with mock_aws: 

        dynamodb = boto3.resource('dynamodb')
    
    #Get existing table 'Website_Hits" 
        table = dynamodb.Table('Website_Hits')

    #Check if there is existing record and update count
        views = table.get_item(Key={'count_id': 'site_hits'})

        curent_views = views['Item']['total_views']
        updated_views = curent_views + 1

        table.put_item(Item={'count_id':'site_hits', 'total_views':updated_views})


    #CORS headers 
    headers = {
        "Access-Control-Allow-Origin": "*", 
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        }


    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({"total_views":str(updated_views)
        })}

