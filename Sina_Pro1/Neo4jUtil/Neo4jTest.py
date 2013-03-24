#-*-coding:utf-8-*-
'''
Created on 2013-3-24

@author: cheng
'''
from py2neo import neo4j,cypher

NEO_ROOT="http://localhost:7474/db/data/"
graph_db=neo4j.GraphDatabaseService(NEO_ROOT)

def IndexTest(uid):
    query="start n=node:Id(id='"+uid+"') return count(n)"
    returnData,metaData=cypher.execute(graph_db, query)
    print type(returnData[0][0])

def NodeTest():
    query="start n=node"

if __name__=="__main__":
    IndexTest("1343")