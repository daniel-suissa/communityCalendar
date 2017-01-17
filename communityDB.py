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

#toolbox functions
def printDB(collection):
    cursor = collection.find({})
    for document in cursor: 
        pprint(document)
def update_internal_list(id, coll, new_elem , field_name):
    document = dict(coll.find_one({'_id': id}))
    #new_list = document[field_name].append(new_elem)
    coll.find_one_and_update({'_id': id}, {'$push': {field_name: new_elem}})

#initialization functions
def communityInit(adminID):
    #change structure of subcommunity within community (maybe use a dictionary)
    dic = {
   "_id": ObjectId(),
   "name": 'Bronfman', 
   "description": 'desc',
   "tags": [], #derived from subcommunity tags
   "godmins": [adminID],
   "sub_communities": [
      {
         "_id" : ObjectId(),
         "name":'Mishelanu',
         "tags": [],
         "admins": [], #ids of users that are admins
         "members" : [], #ids of members
         "membership_requests":[], #ids of users that want to join this community
      },
      {
         "_id" : ObjectId(),
         "name":'All Communities',
         "tags": [],
         "admins": [], #ids of users that are admins
         "members" : [], #ids of members
         "membership_requests":[], #ids of users that want to join this community
      }
   ]
}
    return dic
def eventsInit():
    lst = [
           {
            '_id' : ObjectId(),
            "title": "TestEvent1",
            "location":{
                        "address" : "someAddress 123",
                        "lon": 12.12321,
                        "lat": 43.123123
                             },
            'start_time': datetime.datetime(2017, 10, 27, 6, 0, 0),
            'end_time': datetime.datetime(2017, 10, 27, 8, 0, 0),
            'subcommunities' : [],
            'communities': [] #auto filled by subcommunities
             }
           ]
    return lst

def userInit():
    users = [{
    "_id": ObjectId(),
    "first_name": "userTest1",
    "last_name": "lastTest1",
    "username": "usr1",
    "password": "12345",
    "email": "useremail1@gmail.com",
    "tags": [],
    "admin_of": []
    },{
    "_id": ObjectId(),
    "first_name": "userTest2",
    "last_name": "lastTest2",
    "username": "usr2",
    "password": "56789",
    "email": "useremail2@gmail.com",
    "tags": [],
    "admin_of": []
    }
    ]
    return users
    
    
def insertInitialData():
    if db.count != 0:
        db['community'].drop()
        db['users'].drop()
        db['events'].drop()
    users = userInit()
    godmin = users[0]
    db['users'].insert_many(users)
    firstCom = communityInit(godmin['_id'])
    db['community'].insert_one(firstCom)
    update_internal_list(godmin['_id'],db.users,firstCom['_id'], 'admin_of')
    testEvent = eventsInit()
    testEventId = testEvent[0]['_id']
    db['events'].insert_many(testEvent)
    update_internal_list(testEventId, db.events,firstCom['_id'], 'communities')
    update_internal_list(testEventId, db.events,firstCom['sub_communities'][0]['_id'], 'subcommunities')
    #db['user']
    #db['events']

#api functions
def getCommunity(name):
    return dumps(db[name])
def getAllCommunities():
    lst = []
    cur = db.community.find()
    for col in cur:
        lst.append(col)
    return dumps(lst)
def createEvent(adminID,communityID,subCommunityID,title,address,lon,lat,start_time,end_time):
    print("trying to create event")
    #verifying that the community id and sub comuunity id match each other and exist
    com = db.community.find_one({'_id': ObjectId(communityID)})
    sub_com = db.community.find_one({'_id': ObjectId(communityID)}, { 'sub_communities' : {'$elemMatch' : {'_id': ObjectId(subCommunityID)}}})
    '''
    for sub_rec in com['sub_communities']:
        print("comparing id in collection: ", str(sub_rec['_id']), " to: ",  subCommunityID)
        if str(sub_rec['_id']) == subCommunityID:
            sub_com = sub_rec
    pprint(sub_com)
    pprint(com)
    '''
    if sub_com == None or com == None:
        return 'Error when trying to find community'
    
    #checking the user is authorized to create event 
    if ObjectId(adminID) in sub_com['sub_communities'][0]['admins'] or ObjectId(adminID) in com['godmins']:
        try:
            newEvent = {
     "title": title,
     "location":{
                 "address" : address,
                 "lon": lon,
                 "lat": lat
                 },
     'start_time': start_time,
     'end_time': end_time,
     'subcommunities' : [ObjectId(subCommunityID)],
    'communities': [ObjectId(communityID)] 
    }
            db['events'].insert_one(newEvent)
            printDB(db.events)
            return "created event successfully"
        except:
            return "unable to create event"
    else:
        return "unauthorized user to create event"

#user functions


insertInitialData()
print (db.community)
printDB(db.community)
printDB(db.users)
printDB(db.events)
print("communityDB imported successfully\n\n")
