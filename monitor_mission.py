from MySQL_Modules import article,del_article
from mvknow_init import db
import time

while True:
    time.sleep(180)
    while True:
        print('开始自动下线有阅读次数限制的文章')
        Article_list = article.query.order_by(article.created_date.desc())
        for i in Article_list:
            if i.read_limit is None:
                pass
            elif i.read_num >= i.read_limit:
                del_article_row = del_article(id=i.id, title=i.title, body=i.body,
                                              created_date=i.created_date, author=i.author,
                                              read_num=i.read_num, abstract=i.abstract,read_limit=i.read_limit)
                db.session.add(del_article_row)
                db.session.delete(i)
                db.session.commit()
            else:
                pass

