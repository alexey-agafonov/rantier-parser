#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import os


def _connect_to_db(url: str, db: str) -> MongoClient:
    return MongoClient(url)[db]


db_user = os.environ.get('DB_USER')
print(db_user)
db_password = os.environ.get('DB_PASSWORD')
print(db_password)
db_url = f'mongodb+srv://{db_user}:{db_password}@rantier-55muu.mongodb.net/testretryWrites=true&w=majority'
db_name = 'rantier'
db = _connect_to_db(db_url, db_name)

__all__ = ['db']
