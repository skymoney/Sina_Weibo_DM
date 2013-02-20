#-*-coding:utf-8-*-
'''
Created on 2013-2-17

@author: moneyc
'''
import urllib
import json

url="https://api.weibo.com/2/users/show.json?uid=1648836677&access_token=2.00xj2anBcbu_3Cdac721cd58Gkbe2B"

def getFriends(uid):
    #get id of users who follows the user given uid
    #(uid)<-[follow]-[users]
    URL="https://api.weibo.com/2/friendships/followers/ids.json"
    params="uid"+str(uid)+"&access_token=2.00xj2anBcbu_3Cdac721cd58Gkbe2B"
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    print jsondata

def getFollowUsers(uid):
    #get users the user follows given uid
    #(uid)-[follow]->[users]
    URL="https://api.weibo.com/2/friendships/friends/ids.json"
    params="uid"+str(uid)+"&access_token=2.00xj2anBcbu_3Cdac721cd58Gkbe2B"
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    print jsondata

def getTags(uid):
    #get tags of one specified user given uid
    URL="https://api.weibo.com/2/tags.json"
    params="uid="+str(uid)+"&access_token=2.00xj2anBcbu_3Cdac721cd58Gkbe2B"
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    for tag_single in jsondata:
        print tag_single

if __name__=="__main__":
    content=urllib.urlopen(url)
    jsondata=content.read()
    decode_data=json.loads(jsondata)
    print decode_data
    #getTags(decode_data["id"])
    getFollowUsers(decode_data["id"])