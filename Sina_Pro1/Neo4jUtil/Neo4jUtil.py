#-*-coding:utf-8-*-
'''
Created on 2013-3-24

@author: cheng
'''
from py2neo import neo4j,cypher

NEO_ROOT="http://localhost:7474/db/data/"
graph_db=neo4j.GraphDatabaseService(NEO_ROOT)

def ini():
    id_index=graph_db.get_or_create_index(neo4j.Node,"Id")
    return id_index

def DbExist(uid):
    query="start n=node:Id(id='"+uid+"') return count(n);"
    data,metadata=cypher.execute(graph_db, query)
    #print data
    if data[0][0]==0:
        return False
    return True


def InsertDataBase(userInfo):
    #insert data into databsae
    #format:list
    #[id,name,location,[tag,weight],...]  
    id_index=ini()  
    tag_index=3
    tag_info=""
    while tag_index<len(userInfo):
        tag_single=userInfo[tag_index]
        tag_info+=str(tag_single[0])+"#"+str(tag_single[1])+"$"
        tag_index+=1
    if DbExist(userInfo[0])<>True:
        node=graph_db.create(
        {'id':userInfo[0],
         'name':userInfo[1],
         'location':userInfo[2],
         'tag_info':tag_info[0:len(tag_info)-1]})
        print node[0]
        id_index.add("id",userInfo[0],node[0])
    else:
        query="start n=node:Id(id='"+userInfo[0]+"') return n;"
        data,metadata=cypher.execute(graph_db, query)
        node=data[0][0]
    return node

def creatRelation(fromid,toid,rel=None):
    fromNode=getNode(fromid)
    toNode=getNode(toid)
    fromNode.create_relationship_to(toNode,rel)


def getNode(uid):
    query="start n=node:Id(id='"+uid+"') return n;"
    data,metadata=cypher.execute(graph_db, query)
    return data[0][0]
    