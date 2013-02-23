#-*-coding:utf-8-*-
'''
Created on 2013-2-17

@author: moneyc
'''
import urllib,ConfigParser
import json
from py2neo import neo4j,cypher

NEO_ROOT="http://localhost:7474/db/data/"

def getAccessToken():
    cf=ConfigParser.ConfigParser()
    cf.read("property.config")
    token=cf.get("app info","token")
    return token

def IsExist(dataList,uid):
    if dataList.count(uid)==0:
        return False
    else:
        return True

def getUserInfo(uid,token=None):
    #get user info given uid
    URL="https://api.weibo.com/2/users/show.json"
    params="uid="+uid+"&access_token="+token
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    return jsondata
    
def getFriends(uid,token=None):
    #get id of users who follows the user given uid
    #(uid)<-[follow]-[users]
    URL="https://api.weibo.com/2/friendships/followers/ids.json"
    params="uid"+uid+"&access_token="+token
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    #print jsondata['ids']
    return jsondata['ids']

def getFollowUsers(uid,token=None):
    #get users the user follows given uid
    #(uid)-[follow]->[users]
    URL="https://api.weibo.com/2/friendships/friends/ids.json"
    params="uid"+uid+"&access_token="+token
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    return jsondata['ids']

def getTags(uid,token=None):
    #get tags of one specified user given uid
    URL="https://api.weibo.com/2/tags.json"
    params="uid="+uid+"&access_token="+token
    content=urllib.urlopen(URL+"?"+params)
    jsondata=json.loads(content.read())
    return jsondata
        
def InserDataBase():
    #insert data into databsae
    pass

def grabdata(uid,token=None):
    #start grab data given one uid
    id_set=[]
    id_set.append(uid)
    index=0
    while index<len(id_set):
        current_id=id_set[index]        
        #add uncrawed id into id_list
        '''
        if len(id_set)<=50:
            current_id_friends=getFriends(uid,token)
            for current_friend_id in current_id_friends:
                if IsExist(id_set,current_friend_id)<>True:
                    id_set.append(str(current_friend_id))
        '''
        content=getUserInfo(current_id,token)
        print content['name'],content['location']
        tag_data=getTags(current_id,token)
        #print tag_data
        for tag_single in tag_data:
            for tag in tag_single:
                print tag,tag_single[tag]
        index+=1
    pass

if __name__=="__main__":
    token=getAccessToken()
    #uid=1648836677
    uid="1648836677"
    grabdata(uid,token)