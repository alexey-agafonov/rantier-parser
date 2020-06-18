#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import pymongo
import requests
import os


def connect_to_db(url: str, db_name: str) -> MongoClient:
    return MongoClient(url)[db_name]


def get_realty(login: str, token: str) -> []:
    data = list(db['city'].find({'is_supported': True}))
    cities = ''
    for city in data:
        cities += f'{city["name"]}|'

    result = requests.get("https://ads-api.ru/main/api",
                          params={'user': login,
                                  'token': token,
                                  'category_id': '2',
                                  'city': cities,
                                  'nedvigimost_type': '2',
                                  'date1': '2020-06-18 15:00:00'
                                  })
    # 'startid':
    # date1 and date2
    return result.json()['data']


def init_app():
    api_login = os.environ.get('API_LOGIN')
    api_token = os.environ.get('API_TOKEN')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_url = f'mongodb+srv://{db_user}:{db_password}@rantier-55muu.mongodb.net/testretryWrites=true&w=majority'
    db_name = 'rantier'

    db = connect_to_db(db_url, db_name)
    realty = get_realty(api_login, api_token)
    bulk_update = db['realty'].initialize_unordered_bulk_op()

    for data in realty:
        bulk_update.find({'avitoid': data['avitoid']}).upsert().update({'$set': data})

    try:
        bulk_update.execute()
    except pymongo.errors.OperationFailure as e:
        print(e.code)
        print(e.details)
