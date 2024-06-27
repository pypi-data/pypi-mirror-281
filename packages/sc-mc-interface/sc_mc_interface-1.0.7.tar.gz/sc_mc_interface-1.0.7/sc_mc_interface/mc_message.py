import requests

def McMessage(store,conversationId,cookie):
    url = 'https://'+store+'/admin/api/sc/mc/message/'+conversationId
    print(url)
    headers = {'cookie': cookie}
    body = {'searchType': 'up'}
    r = requests.get(url=url, headers=headers, params=body).json()
    return r

def McConversation(store,merchantId,channelType,pageSize,thirdChannelIdList,cookie):
    url = 'https://'+store+'/admin/api/sc/mc/conversation'
    print(url)
    headers = {'cookie': cookie}
    body = {"lastPage":False,"precise":False,"merchantId":merchantId,"channelType":channelType,"searchTags":[],"searchType":'chat_history',"pageSize":pageSize,"thirdChannelIdList":thirdChannelIdList,"sortRule":0,"guestMode":True}
    r = requests.post(url=url, headers=headers, json=body).json()
    return r
