#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, url_for, redirect
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
app =Flask(__name__)

class User():
    __tablename__ = "user"
    name = Column(String(80), nullable = False)
    id = Column(Integer,primary_key = True)
    
    @property
    def serialize(self):
        return {
             'id': self.id,
             'name':self.name
        }
@app.route('/testUser', methods=['GET', 'POST'])
def testHandler():
    if(request.method == 'GET'):
        users = ession.query(User).all()
        return jsonify(users = [i.serialize for i in users])
    if(request.method == 'POST'):
        
    
"""
Created on Sat Dec 24 23:30:03 2016

@author: danielsuissa
"""

