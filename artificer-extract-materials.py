import boto3
import requests
import json

API_URL = 'https://gamepress.gg/sites/default/files/aggregatedjson/calc-material-images-FGO.json'
S3_BUCKET = 'artificer-extract'
FILE_NAME = 'materials.json'

bucket = boto3.resource('s3').Bucket(S3_BUCKET)

'''
download_json_from_url

Download json from API, wrap json array in an indexable key 'data' and return json object
'''
def download_json_from_url(url):
    response = requests.get(url)
    json_obj = dict()
    json_obj['data'] = response.json()
    return json_obj

'''
write_json_to_local

Opens a file, writes the json to the file, and closes it
'''
def write_json_to_local(json_obj, local_fpath):
    with open(local_fpath, "w+") as f:
        f.write(json.dumps(json_obj))
        f.close()

'''
upload_json_to_s3

Uploads the json file on the local file system to S3
'''
def upload_file_to_s3(local_file_name, bucket_name, remote_file_name):
    bucket.put_object(Body=str(open(local_file_name, 'r').readline()).encode('utf-8'), Bucket=bucket_name, Key=remote_file_name)

'''
main

Driver function for local execution
'''
def main():
    json_materials = download_json_from_url(API_URL)
    write_json_to_local(json_materials, '/tmp/' + FILE_NAME)
    upload_file_to_s3('/tmp/' + FILE_NAME, S3_BUCKET, FILE_NAME)

'''
lambda_handler

Driver function for lambda execution
'''
def lambda_handler(event, context):
    main()

main()
