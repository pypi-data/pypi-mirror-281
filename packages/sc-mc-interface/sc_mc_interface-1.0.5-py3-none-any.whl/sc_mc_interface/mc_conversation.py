import requests

def McConvertion(store,conversationId,cookie):
    url = 'https://'+store+'/admin/api/sc/mc/message/'+conversationId
    print(url)
    headers = {'cookie': cookie}
    body = {'searchType': 'up'}
    r = requests.get(url=url, headers=headers, params=body).json()
    return r