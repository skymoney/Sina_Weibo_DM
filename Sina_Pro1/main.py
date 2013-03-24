#-*-coding:utf-8-*-
'''
Created on 2013-2-6

@author: moneyc
'''
from weibo import APIClient
import ConfigParser

def getConfig():
    cf=ConfigParser.ConfigParser()
    
    cf.read("property.config")
    
    ops=cf.options("web app info")

def get_access_token(app_key,app_secret,callback_url):
    client=APIClient(app_key=app_key,app_secret=app_secret, redirect_uri=callback_url)
    auth_url=client.get_authorize_url()
    print auth_url
    
    code=raw_input("input code")
    r=client.request_access_token(code)
    access_token=r.access_token
    expire_in=r.expires_in
    print 'access_token:',access_token
    print 'expire in: ',expire_in
    
    return access_token,expire_in

if __name__=="__main__":
    #client=weibo.APIClient()
    cf=ConfigParser.ConfigParser()
    cf.read("property.config")
    
    APP_KEY=cf.get("ad app info","app_key")
    APP_SECRET=cf.get("ad app info","app_secret")
    CALL_URL=cf.get("ad app info","callback_url")
    
    access_token,expire_in=get_access_token(app_key=APP_KEY,app_secret=APP_SECRET,
                           callback_url=CALL_URL)
    print access_token,expire_in
    
    
    
