import boto3



session = boto3.Session(profile_name='dev')
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.

dynamodb = session.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")

table = dynamodb.Table('FourThird')

# client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
#
# response = client.describe_table(
#     TableName='FourThird'
# )

response = table.get_item(
        Key={
            'Keyword': 'manages the for',

        }
    )


len = len(response['Item']['content'])
print(len)