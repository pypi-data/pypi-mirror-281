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

def McConversation_inbox(store,merchantId,channelType,pageSize,cookie):
    url = 'https://'+store+'/admin/api/sc/mc/conversation'
    print(url)
    headers = {'cookie': cookie}
    body = {"lastPage":False,"precise":False,"merchantId":merchantId,"channelType":channelType,"searchTags":[],"searchType":'chat_history',"pageSize":pageSize,"sortRule":0,"guestMode":True}
    r = requests.post(url=url, headers=headers, json=body).json()
    return r

# if __name__ == '__main__':
#     r = McConversation_inbox('dengyingying10001.myshoplinestg.com', '4201795357', 1, 20,
#                        'n_u=18d8bcfb629edcbcb9d0a13bcdc5bd4e; f_ds_info.sig=fvvUgp8T4tMFLk_D84Pdxrm-jFqbf_F5NaozNBXwjdk; store_id=1651564626314; store_id.sig=tQ_x5A3wM3L9J-E19r5tpUIbwDn3oF-_gY3_eIshunc; merchant_id=4201795357; merchant_id.sig=tfpME00x0dNA2lzI3TfBsImV7gprSE4fIckS0BXycyU; currency_code=USD; currency_code.sig=nEGddW1-E-8oJfI_Pm_5XNzC2sMi1n3aVzZ3v01csyY; localization=HK; lang.sig=hjeAuyyZsT_Nyv8gg3V5LyS3803lRMFE4f8Lg-qR8v8; addressLang.sig=2r3OjHSjO8YI7hWp4-5ONoLbf9GNBaM8T0JR_QsQsVM; userSelectLocale.sig=hGryIiLO_uZhO4NAxRDvTPyiRle7Ax1gCJpQrVYcfhk; s_id=69D0E741548A405F1449AAD1B1CDD7F7; s_id.sig=787c1df72afd971fc59953c7b9af871b; a_ste=Dopo7/Z7i3M+3t6Sd89bobUMS0QtlmaDX7/oWRH0LvmdP7iBk+Hz8QL01R3SJKqHb8aFMObih5h5l/EAByfhmg==; r_b_ined=1; _hjSessionUser_3760809=eyJpZCI6IjE5YzlhNWRhLWJhZjgtNTQ0Ni1iNTc1LTFmNmJkYWJiNmUyNCIsImNyZWF0ZWQiOjE3MTUwODQ2NDYwNTMsImV4aXN0aW5nIjp0cnVlfQ==; _BEAMER_USER_ID_FKUpATyQ57438=a95a40fd-bd4a-4777-9234-0796851b2517; _BEAMER_FIRST_VISIT_FKUpATyQ57438=2024-05-07T06:26:43.723Z; _BEAMER_USER_ID_xoATBRYa57439=eb1aac5c-469c-44b9-8959-52d84ce2fc55; _BEAMER_FIRST_VISIT_xoATBRYa57439=2023-09-11T03:22:30.359Z; f_ds_info=qGcC44JZBIMdmn8v6Ot2+VjURdaDhLr7aHmqVNVZQw/aJbVlT1RVY/48mXFye89iYEZKj5kOO+OxU5eNBLt8HQ==; n_sess={"session_id":"1bad061b-3d2b-4f14-8ad3-ab0fa6176363","created_at":1717075431219,"last_session_id":"78ade037-f147-4e8c-92da-05a03296c4e0","session_create_type":102}; a_merchant_behavior_collection=1; hd_newui=0.8948658904058311; _ga=GA1.1.79199183.1718946213; a_lang=zh-hans-cn; ai_kf_language=zh-hans-cn; a_osudb_appid=1163336839; a_osudb_subappid=1; a_osudb_uid=4201795357; a_osudb_oar=#01#SID0000105BNVFxNjQVluxsRb00AJdHL9a2Kubn2nzQaR7u37a7sgXBzCVGyfr5LhmtnCEQekq4xet0HjIHj9Cc840VDgaUAAN2vzEK4UmKoag/4yPHcg5ofs8/W9+fUpRew70sGx+veBX15kZAONjIc+/iBgZcg; a_lce=1720014971716; a_dhch=dengyingying10001; r_b_in=1; _ga_CVZ36HEL2Z=GS1.1.1719457731.14.0.1719457731.0.0.0; _hjSession_3760809=eyJpZCI6ImU0NmVlZjUyLTk1ZWEtNGJhZC05MGRkLWFkZTRiYmU1ZDAwNSIsImMiOjE3MTk0NzQ0MTY5ODEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; hdjs_session_id=0.3766238170955767; hdjs_session_time=1719474428359; JSESSIONID=70273BE6BC7DD301549EACAD65FBE041; log_session_id=bc0e390aa82d1602327e4b93396a6038')
#     print(r)

