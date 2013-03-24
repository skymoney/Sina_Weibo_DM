#-*-coding:utf-8-*-
'''
Created on 2013-2-17

@author: moneyc
'''
import urllib,ConfigParser
import json

from Neo4jUtil import Neo4jUtil


def getAccessToken():
    cf=ConfigParser.ConfigParser()
    cf.read("../property.config")
    token=cf.get("ad app info","token")
    return token

def IsExist(dataList,uid):
    if dataList.count(uid)==0:
        return False
    else:
        return True

#all weibo ops to get data needed

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
    


    
#grap data
def grabdata(uid,token=None):
    #start grab data given one uid
    id_set=[]
    id_set.append(uid)
    index=0
    while index<len(id_set) and index<50:   #in test env, small amount is enough
        current_id=id_set[index]  
        userInfo=[]      
        #add uncrawed id into id_list
        content=getUserInfo(current_id,token)
        userInfo.append(content['idstr'])
        userInfo.append(content['name'])
        userInfo.append(content['location'])
        tag_data=getTags(current_id,token)
        #print tag_data
        
        for tag_single in tag_data:
            tag_single_list=[]
            for tag_key in tag_single:                
                tag_single_list.append(tag_single[tag_key])
            userInfo.append(tag_single_list)
        Neo4jUtil.InsertDataBase(userInfo)
        print 'current user '+current_id+' done....'
        #add more ids into Id Set
        dealFriends(uid,token)
        print 'friends done....'
        dealFollowers(uid,token)
        index+=1

def dealFriends(uid,token=None):
    friends_ids=getFriends(uid,token)
    try:
        for friendId in friends_ids:
            id=str(friendId)
            userInfo=[]
            content=getUserInfo(id,token)
            userInfo.append(content['idstr'])
            userInfo.append(content['name'])
            userInfo.append(content['location'])
            tag_data=getTags(id,token)
            #print tag_data
            
            for tag_single in tag_data:
                tag_single_list=[]
                for tag_key in tag_single:                
                    tag_single_list.append(tag_single[tag_key])
                userInfo.append(tag_single_list)
            node=Neo4jUtil.InsertDataBase(userInfo)
            
            Neo4jUtil.creatRelation(id,uid,"Follows")
    except:
        pass      

def dealFollowers(uid,token=None):
    follow_ids=getFollowUsers(uid,token)
    try:
        for followId in follow_ids:
            id=str(followId)
            userInfo=[]
            content=getUserInfo(id,token)
            userInfo.append(content['idstr'])
            userInfo.append(content['name'])
            userInfo.append(content['location'])
            tag_data=getTags(id,token)
            #print tag_data
            
            for tag_single in tag_data:
                tag_single_list=[]
                for tag_key in tag_single:                
                    tag_single_list.append(tag_single[tag_key])
                userInfo.append(tag_single_list)
            node=Neo4jUtil.InsertDataBase(userInfo)
            
            Neo4jUtil.creatRelation(uid,id,"Follows")
    except:
        pass

if __name__=="__main__":
    token=getAccessToken()
    #uid=1648836677
    uid="1648836677"
    grabdata(uid,token)
    #DbExist(uid)
    #data=getFollowUsers(uid,token)
    #print data