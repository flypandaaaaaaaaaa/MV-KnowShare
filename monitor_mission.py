from MySQL_Modules import article,del_article
from mvknow_init import db
import time
from mvknow_func import GetNowTime

while True:
    time.sleep(10)
    print('开始自动下线有阅读次数限制的文章')
    Article_list = article.query.order_by(article.created_date.desc())
    for i in Article_list:
        if i.read_limit is None:
            print("无阅读次数限制",GetNowTime(),i.title)
        elif i.read_num >= i.read_limit:
            del_article_row = del_article(id=i.id, title=i.title, body=i.body,
                                          created_date=i.created_date, author=i.author,
                                          read_num=i.read_num, abstract=i.abstract,read_limit=i.read_limit,read_public=i.read_public)
            db.session.add(del_article_row)
            db.session.delete(i)
            db.session.commit()
            print('文章到达阅读次数限制，下线成功',GetNowTime(),i.title)
        else:
            print('文章还未到达阅读次数限制',GetNowTime(),i.title)

