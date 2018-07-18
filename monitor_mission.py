from MySQL_Modules import article,del_article
from mvknow_init import db
import time
from mvknow_func import GetNowTime
from move_article import mv_article
while True:
    time.sleep(10)
    print('开始自动下线有阅读次数限制的文章')
    Article_list = article.query.order_by(article.created_date.desc())
    for i in Article_list:
        if i.read_limit is None:
            print("无阅读次数限制",GetNowTime(),i.title)
        elif int(i.read_num) >= int(i.read_limit):
            mv_article(i.id).offline_article()
            print('文章到达阅读次数限制，下线成功',GetNowTime(),i.title)
        else:
            print('文章还未到达阅读次数限制',GetNowTime(),i.title)

