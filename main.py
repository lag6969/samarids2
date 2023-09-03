import json
import requests
from time import time as timestamp
from datetime import datetime
from time import sleep
import base64
from json_minify import json_minify
# from aminofix import objects
from concurrent.futures import  ThreadPoolExecutor,ProcessPoolExecutor
from binascii import hexlify
from os import path
import json
import os
from uuid import UUID
import random
import hmac
from os import urandom
from pytz import timezone
from functools import reduce
from base64 import b64decode, b64encode
from typing import Union
from hashlib import sha1
from hmac import new
import sys
#sys.stdin.reconfigure(encoding='utf-8')
#sys.stdout.reconfigure(encoding='utf-8')
from itertools import cycle
 
THIS_FOLDER = path.dirname(path.abspath(__file__))
account_file = path.join(THIS_FOLDER, "ids2.json")
secrets=[]
 
with open(account_file) as file:
    secrets = json.load(file)
 
import json
 
 
PREFIX = bytes.fromhex("19")
SIG_KEY = bytes.fromhex("DFA5ED192DDA6E88A12FE12130DC6206B1251E44")
DEVICE_KEY = bytes.fromhex("E7309ECC0953C6FA60005B2765F99DBBC965C8E9")
count=0
links = [
    "https://proxy69.vercel.app/proxy?url="
]
 
comids=['205677143']
 
list_com=cycle(comids)
 
logins = cycle(links)
 
api="https://service.aminoapps.com/api/v1"
 
def get_com():
    
      return next(list_com)
 
 
def get_total(sid):
    try:
        response = requests.get(f"{next(logins)}{api}/g/s/wallet", headers=get_headers(sid))
        if response.status_code==200:
                resp=json.loads(response.text)
                coins=resp["wallet"]["totalCoins"]
                return coins
        elif response.status_code==403:
                return get_total(sid)
        else:
                print(json.loads(response.text)["api:message"])
                return 80
    except requests.exceptions.ProxyError as e:
            return get_total(sid)
    
def collect(sid,coins,em,chatId):
    
    try:
        transactionId = str(UUID(hexlify(urandom(16)).decode('ascii')))
        data = {
                "coins": coins,
                "tippingContext": {"transactionId": transactionId},
                "timestamp": int(timestamp() * 1000)
            }
        
        url = f"{next(logins)}{api}/g/s/chat/thread/{chatId}/tipping"
        data = json.dumps(data)
        response = requests.post(url, headers=get_headers(sid,data), data=data)
        if response.status_code==200:
                resp=json.loads(response.text)
                if resp['api:message']=='OK':
                        print(f'collected {coins}')
        elif response.status_code==403:
                return collect(sid,coins,em,chatId)
        else:
                print(json.loads(response.text)["api:message"])
                return None
    except requests.exceptions.ProxyError as e:
             return collect(sid,coins,em,chatId)
 
def tzFilter(hour: int = 23, tz: str = None) -> int:
 
    zones = ["Etc/GMT" + (f"+{i}" if i > 0 else f"{i}") for i in range(-12, 12)]
 
    return next(
        int(datetime.now(timezone(_)).strftime("%Z").replace("GMT", "00")) * 60
        for _ in ([tz] if tz else zones)
        if (tz or (int(datetime.now(timezone(_)).strftime("%H")) == hour))
    )
 
 
def gen_deviceId(data: bytes = None) -> str:
    if isinstance(data, str):
        data = bytes(data, 'utf-8')
    identifier = PREFIX + (data or os.urandom(20))
    mac = hmac.new(DEVICE_KEY, identifier, sha1)
    return f"{identifier.hex()}{mac.hexdigest()}".upper()
 
def sig(data: Union[str, bytes]) -> str:
    data = data if isinstance(data, bytes) else data.encode("utf-8")
    signature = hmac.new(SIG_KEY, data, sha1)
    return b64encode(PREFIX + signature.digest()).decode("utf-8")
 
def get_total(sid):
    
    response = requests.get(f"{next(logins)}{api}/g/s/wallet", headers=get_headers(sid))
    if response.status_code==200:
            resp=json.loads(response.text)
            coins=resp["wallet"]["totalCoins"]
            return coins
    elif response.status_code==403:
             get_total(sid)
    else:
            print(json.loads(response.text)["api:message"])
            return 80
    
    
    
 
def get_headers(sid=None,data=None):
    headers={
    'Accept-Language': 'en-US', 
    'Content-Type': 'application/x-www-form-urlencoded', 
    'User-Agent': 'Apple iPhone12,1 iOS v15.5 Main/3.12.2', 
    #'Host': 'service.aminoapps.com', 
    'Accept-Encoding': 'gzip',
    'Connection': 'Upgrade',
    'NDCDEVICEID':gen_deviceId()
    }
    if sid:
        headers['NDCAUTH']=f"sid={sid}"
    if data:
        headers["NDC-MSG-SIG"]=sig(data)
        headers["Content-Length"] = str(len(data))
    return headers
 
 
def collect(sid,coins,em,chatId):
    
 
    transactionId = str(UUID(hexlify(urandom(16)).decode('ascii')))
    data = {
            "coins": coins,
            "tippingContext": {"transactionId": transactionId},
            "timestamp": int(timestamp() * 1000)
        }
    
    url = f"{next(logins)}{api}/g/s/chat/thread/{chatId}/tipping"
    data = json.dumps(data)
    response = requests.post(url, headers=get_headers(sid,data), data=data)
    if response.status_code==200:
            resp=json.loads(response.text)
            if resp['api:message']=='OK':
                    print(f'collected {coins}')
    elif response.status_code==403:
             collect(sid,coins,em,chatId)
    else:
             print(json.loads(response.text)["api:message"])
             return None
 
def login_custom(email: str, secret: str):
        
        try:
            data = json.dumps({
                "email": email,
                # "phoneNumber":email,
                "v": 2,
                "secret":f"{secret}",
                "deviceID":gen_deviceId(),
                "clientType": 100,
                "action": "normal",
                "timestamp": int(timestamp() * 1000)
            })
            
            
            response = requests.post(f"{next(logins)}{api}/g/s/auth/login", headers=get_headers(data=data), data=data)
            #print(response.text)
            if response.status_code==200:
                
                return json.loads(response.text)["sid"]
            elif response.status_code==403:
                return login_custom(email,secret)
            else:
                print(response.text)
                return None
        except requests.exceptions.ProxyError as e:
             print(e)
             #return login_custom(email,secret)
 
 
 
#def join_com(sid,m,comId):
        #try:
            #data = {"timestamp": int(timestamp() * 1000)}
            #data = json.dumps(data)
            
            #response = requests.post(f"{next(logins)}{api}/x{comId}/s/community/join", data=data, headers=get_headers(sid,data))
            #if response.status_code==200:
                #resp=json.loads(response.text)
                #if resp['api:message']=='OK':
                        #print(f'joined community: {m}')
                        #return True
                #else: return False
            #elif response.status_code==403:
                #return join_com(sid,m,comId)
            #else:
                #  print(json.loads(response.text)["api:message"])
                 #return False
                # comid.clear()
                # comid.append("52193277")
                # join_com(sid,comid[0])
            
        #except:
              #return join_com(sid,m,comId)
 
#def leave_com(sid, m,comId):
        
        #response = requests.post(f"{next(logins)}{api}/x{comId}/s/community/leave", headers=get_headers(sid))
        #if response.status_code != 200: 
            #return True
        #else:
            # return leave_com(sid,m,comId)
 
 
def magic_num():
    timing = {"start": int(datetime.timestamp(datetime.now())), "end": int(datetime.timestamp(datetime.now())) + 300}
    return timing
 
 
def gen(sid,i,m,comId):
 try:
    
    chunk=[magic_num() for a in range(35)]
    data = {"userActiveTimeChunkList": chunk,"timestamp": int(timestamp() * 1000),"optInAdsFlags": 2147483647,"timezone":190}
    data = json_minify(json.dumps(data))
    response = requests.post(f"{next(logins)}{api}/x{comId}/s/community/stats/user-active-time", headers=get_headers(sid,data), data=data)
    if response.status_code==200:
              
              print(f'{json.loads(response.text)["api:message"]} {m} --- {i}')
              #print(pp)
    
    else:
             
             print(json.loads(response.text)["api:message"])
    return None
    
    
 except requests.exceptions.ProxyError as e:
      gen(sid,i,m,comId)
    
def gen_1(account):
        
        # if put.find_one({"email":account['email']}) is None:
                          
            sid=login_custom(account['email'],account['secret'])
            
            if sid:
                    
                    # dict={"email":account['email'],"secret":account['secret']}
                    # put.insert_one(dict)
                    m=account['email']
                    print(f"logged in {m}")
                    id_com=get_com()
                    
                    
                    #com=join_com(sid,m,id_com)
                    #if com:
                            
                    for i in range(1,24,1):
                                gen(sid,i,m,id_com)
                                sleep(1)
                            #leave_com(sid,m,id_com)
            else:
                pass
                
        
 
 
 
for em in secrets:
      gen_1(em)
