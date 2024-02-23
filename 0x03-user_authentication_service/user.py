#!/usr/bin/env python3
"""Class User for ORM"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME, INTEGER


base = declarative_base()


class User(base):
    '''
    user db class
    '''
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
