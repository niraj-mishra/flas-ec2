from flask import Flask,jsonify
import boto3
import botocore
import sys
import os

app = Flask(__name__)

aws=boto3.session.Session(profile_name=None)
iam=boto3.client('iam',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))


#Endpoints (\) for the app
@app.route('/')
def endpoints():
    return "<html>Feature List<br><br> localhost:5000/users/list <br> localhost:5000/users/tags/user_name <br> localhost:5000/users/keys/user_name </html>"


#Endpoints (/users/list) for the app
@app.route('/users/list')
def list_users():
    IAMusers={}
    count=1
    UserList=iam.get_paginator('list_users')
    
    for user in UserList.paginate():
        for each_user in user['Users']:
                IAMusers[count]=each_user['UserName']
                count +=1
        return jsonify(IAMusers)

#Endpoints (/users/tags/username) for the app
@app.route('/users/tags/<string:user>')
def list_users_tags(user):
    User_tags = {}
    count=1
    if len(iam.list_user_tags(UserName=user))!=0:
        for tag in iam.list_user_tags(UserName=user)['Tags']:
                User_tags[count]={}
                User_tags[count]["Key"]=tag['Key']
                User_tags[count]["Value"]=tag['Value']
                count+=1
        return jsonify(User_tags)

#Endpoints (/users/keys/username) for the app
@app.route('/users/keys/<string:user>')
def list_users_keys(user):
    access_keys = {}
    count=1
    if len(iam.list_access_keys(UserName=user)['AccessKeyMetadata'])!=0:
            for key in iam.list_access_keys(UserName=user)['AccessKeyMetadata']:
                if "LastUsedDate" in iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])['AccessKeyLastUsed']:
                    LastUsedDate=iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])['AccessKeyLastUsed']['LastUsedDate'].strftime("%d-%m-%Y %H:%M")
                else:
                     LastUsedDate="not used"
                access_keys[count]={}
                access_keys[count]['AccessKeyId']=key['AccessKeyId']
                access_keys[count]['CreateDate']=key['CreateDate'].strftime("%d-%m-%Y %H:%M")
                access_keys[count]['AccessKeyLastUsed']=LastUsedDate
            
                count +=1
            return jsonify(access_keys)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
