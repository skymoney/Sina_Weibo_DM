#-*-coding:utf-8-*-
'''
Created on 2013-2-17

@author: moneyc
'''
import urllib,ConfigParser
import json


def getAccessToken():
    cf=ConfigParser.ConfigParser()
    cf.read("property.config")
    token=cf.get("app info","token")
    return token

def getFriends(uid,token=None):
    #get id of users who follows the user given uid
    #(uid)<-[follow]-[users]
    URL="https://api.weibo.com/2/friendships/followers/ids.json"
    params="uid"+str(uid)+"&access_token="+token
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    print jsondata

def getFollowUsers(uid,token=None):
    #get users the user follows given uid
    #(uid)-[follow]->[users]
    URL="https://api.weibo.com/2/friendships/friends/ids.json"
    params="uid"+str(uid)+"&access_token="+token
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    print jsondata

def getTags(uid,token=None):
    #get tags of one specified user given uid
    URL="https://api.weibo.com/2/tags.json"
    params="uid="+str(uid)+"&access_token="+token
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    for tag_single in jsondata:
        print tag_single

if __name__=="__main__":
    token=getAccessToken()
    url="https://api.weibo.com/2/users/show.json?uid=1648836677&access_token="+token
    content=urllib.urlopen(url)
    jsondata=content.read()
    decode_data=json.loads(jsondata)
    #getTags(decode_data["id"])
    #getFollowUsers(decode_data["id"])
    
    getTags(decode_data["id"],token)