#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 18:20:23 2016

@author: danielsuissa
"""
# community

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from pprint import pprint
import datetime


client = MongoClient()
db = client['CommunityCalendar']
print('\n',db.CommunityCalendar.count())

def printDB(collection):
    cursor = collection.find({})
    for document in cursor: 
        pprint(document)
def communityInit(adminID):
    #change structure of subcommunity within community (maybe use a dictionary)
    dic = {
   "_id": ObjectId(),
   "name": 'Bronfman', 
   "description": 'desc',
   "tags": [],
    "godmins": [adminID],
   "sub_communities": [
      {
         "_id" : ObjectId(),
         "name":'Mishelanu',
         "tags": [],
         "admins": []
      },
      {
         "_id" : ObjectId(),
         "name":'Parent',
         "tags": [],
         "admins": []
      }
   ],
   "events":
       [
        {
         "title": "TestEvent1",
         "location":{
                     "address" : "someAddress 123",
                     "lon": 12.12321,
                     "lat": 43.123123
                     },
         'start_time': datetime.datetime(2017, 10, 27, 6, 0, 0),
         'end_time': datetime.datetime(2017, 10, 27, 8, 0, 0)
        }
    ]
}
    return dic

def userInit():
    users = [{
    "_id": ObjectId(),
    "name": "userTest1",
    "username": "usr1",
    "password": "12345",
    "email": "useremail1@gmail.com",
    "tags": []
    },{
    "_id": ObjectId(),
    "name": "userTest2",
    "username": "usr2",
    "password": "56789",
    "email": "useremail2@gmail.com",
    "tags": []
    }
    ]
    return users
    
    
def insertInitialData():
    if db.count != 0:
        db['community'].drop()
        db['users'].drop()
    users = userInit()
    godmin = users[0]
    db['users'].insert_many(users)
    db['community'].insert_one(communityInit(godmin['_id']))
    
    #db['user']
    #db['events']

def getCommunity(name):
    return dumps(db[name])
def getAllCommunities():
    lst = []
    cur = db.community.find()
    for col in cur:
        lst.append(col)
    return dumps(lst)
def createEvent(adminID,communityID,subCommunityID,title,address,lon,lat,start_time,end_time):
    #find community
    print("trying to create event")
    print("comparing the community: " , communityID)
    com = db.community.find_one({"_id": ObjectId(communityID)})
    if com != None:
        sub_com = None
        for sub in com['sub_communities']:
            print("checking for sub community " , sub['_id'], end="\n")
            if  ObjectId(subCommunityID) == sub['_id']:
                sub_com = sub
        if sub_com != None:
            if ObjectId(adminID) in sub_com['admins'] or ObjectId(adminID)  in com['godmins']:
                try:
                            sub_c.insert_one({
             "title": title,
             "location":{
                         "address" : address,
                         "lon": lon,
                         "lat": lat
                         },
             'start_time': start_time,
             'end_time': end_time
            })
                            return "created event successfully"
                except:
                    return "unable to create event"
            else:
                return "unauthorizes user to create event"
        else:
            return "couldn't find subcommunity"
    else:
        return "couldn't find community"
#user functions


insertInitialData()
print (db.community)
printDB(db.community)
print("communityDB imported successfully\n\n")
'''
{
   _id: COMMUNITY_ID
   name: NAME_OF_COMMUNITY, 
   description: COMMUNITY_DESCRIPTION,
   admin: [] #dependency ADMIN_ID,
   url: URL_OF_COMMUNITY,
   tags: [],
   sub_community: [	
      {
         _id = SUBCOMMUNITY
         user:'COMMENT_BY',
         message: TEXT,
         dateCreated: DATE_TIME,
         like: LIKES 
      },
      {
         user:'COMMENT_BY',
         message: TEXT,
         dateCreated: DATE_TIME,
         like: LIKES
      }
   ]
}
'''
#user