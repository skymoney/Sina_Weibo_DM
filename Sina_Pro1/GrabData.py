#-*-coding:utf-8-*-
'''
Created on 2013-2-17

@author: moneyc
'''
import urllib,ConfigParser
import json
from py2neo import neo4j,cypher

NEO_ROOT="http://localhost:7474/db/data/"
graph_db=neo4j.GraphDatabaseService(NEO_ROOT)

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
    
def DbExist(uid):
    query="start n=node:id(id="+uid+") return n;"
    #data,metadata=cypher.execute(graph_db, query)
    #print data
    return False
      
def InsertDataBase(userInfo):
    #insert data into databsae
    #format:list
    #[id,name,location,[tag,weight],...]    
    tag_index=3
    tag_info=""
    while tag_index<len(userInfo):
        tag_single=userInfo[tag_index]
        tag_info+=tag_single[0]+"#"+str(tag_single[1])+"$"
        tag_index+=1
    if DbExist(userInfo[0])<>True:
        node=graph_db.create(
        {'id':userInfo[0],
         'name':userInfo[1],
         'location':userInfo[2],
         'tag_info':tag_info[0:len(tag_info)-1]})
    
    print 'current user insert done...'
    

def grabdata(uid,token=None):
    #start grab data given one uid
    id_set=[]
    id_set.append(uid)
    index=0
    while index<len(id_set):
        current_id=id_set[index]  
        userInfo=[]      
        #add uncrawed id into id_list
        '''
        if len(id_set)<=50:
            current_id_friends=getFriends(uid,token)
            for current_friend_id in current_id_friends:
                if IsExist(id_set,current_friend_id)<>True:
                    id_set.append(str(current_friend_id))
        '''
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
        InsertDataBase(userInfo)
        index+=1
    

if __name__=="__main__":
    token=getAccessToken()
    #uid=1648836677
    uid="1648836677"
    grabdata(uid,token)
    #DbExist(uid)