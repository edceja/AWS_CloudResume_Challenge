import json
import boto3


def lambda_handler(event, context):

    #Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    
    #Get existing table 'Website_Hits" 
    table = dynamodb.Table('Website_Hits')

    #Check if there is existing record and update count
    try:
        views = table.get_item(Key={'hits': 'site_hits'})

        curent_views = views['Item']['total_views']
        updated_views = curent_views + 1

        table.put_item(Item={'hits':'site_hits', 'total_views':updated_views})

    #Update the count to 1 if no record exists 
    except: 
        table.put_item(Item={'hits':'site_hits', 'total_views':1})

        updated_views = 1

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

