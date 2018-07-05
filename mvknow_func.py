import time
from MySQL_Modules import article
def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M",time.localtime(time.time()))

def GetIDList(page,perpage):
    Article_list = article.query.filter(article.read_public=='Y').order_by(article.id.desc())
    IDList=[]
    for i in Article_list:
        IDList.append(i.id)
    return IDList[perpage*page-perpage:perpage*page]