#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 11:36:27 2017

@author: danielsuissa
"""

from flask import Flask, render_template, request, session, url_for, redirect
import communityDB

app = Flask(__name__)
@app.route('/', methods = ['GET','POST'])
def index():
    return '0'
@app.route('/communityList', methods = ['GET','POST'])
def communityList():
    return communityDB.getAllCommunities()
@app.route('/insertEvent', methods = ['POST'])
def insertEvent():
    print("function called")
    adminID = request.args.get('adminID')
    communityID = request.args.get('communityID')
    subCommunityID = request.args.get('subCommunityID')
    address = request.args.get('address')
    lon = request.args.get('lon')
    lat = request.args.get('lat')
    title = request.args.get('title')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    return communityDB.createEvent(adminID,communityID,subCommunityID,title,address,lon,lat,start_time,end_time)
if __name__ == "__main__":
    app.run()