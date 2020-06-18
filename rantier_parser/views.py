#!/usr/bin/env python

from aiohttp import web
import os
from pymongo import MongoClient
import pymongo
import requests


async def index(request):
    api_login = os.environ.get('API_LOGIN')
    api_token = os.environ.get('API_TOKEN')
    print(api_login)
    print(api_token)
    db_user = os.environ.get('DB_USER')
    print(db_user)
    db_password = os.environ.get('DB_PASSWORD')
    print(db_password)
    db_url = f'mongodb+srv://{db_user}:{db_password}@rantier-55muu.mongodb.net/testretryWrites=true&w=majority'
    db_name = 'rantier'
    db = MongoClient(db_url)[db_name]

    # realty = get_realty(api_login, api_token)

    data = list(db['city'].find({'is_supported': True}))
    cities = ''
    for city in data:
        cities += f'{city["name"]}|'

    realty = requests.get("https://ads-api.ru/main/api",
                          params={'user': api_login,
                                  'token': api_token,
                                  'category_id': '2',
                                  'city': cities,
                                  'nedvigimost_type': '2',
                                  'date1': '2020-06-18 15:00:00'
                                  })

    bulk_update = db['realty'].initialize_unordered_bulk_op()

    for data in realty:
        bulk_update.find({'avitoid': data['avitoid']}).upsert().update({'$set': data})

    try:
        bulk_update.execute()
    except pymongo.errors.OperationFailure as e:
        print(e.code)
        print(e.details)

    return web.Response(text='Hello, World!')
