from MySQL_Modules import article,del_article
from mvknow_init import db


class move_article(object):
    """
    online-offiline the article
    """
    def __init__(self,article_id):
        self.article_id=article_id
    def offline_article(self):
        Article=article.query.filter_by(id=self.article_id).first()
        Del_article = del_article.query.filter_by(id=self.article_id).first()
        if Del_article is None:
            del_article_row = del_article(id=Article.id, title=Article.title, body=Article.body,
                                          created_date=Article.created_date, author=Article.author,
                                          read_num=Article.read_num, abstract=Article.abstract,
                                          read_limit=Article.read_limit, read_public=Article.read_public)
            db.session.add(del_article_row)
            db.session.delete(Article)
            db.session.commit()
        elif Del_article.id != 0:
            pass
    def online_article(self):
        Article = article.query.filter_by(id=self.article_id).first()
        Del_article = del_article.query.filter_by(id=self.article_id).first()
        if Article is None:
            article_row = article(id=Del_article.id, title=Del_article.title, body=Del_article.body,
                                  created_date=Del_article.created_date, author=Del_article.author,
                                  read_num=0, abstract=Del_article.abstract, read_limit=Del_article.read_limit,
                                  read_public=Del_article.read_public)
            db.session.add(article_row)
            db.session.delete(Del_article)
            db.session.commit()
        elif Article.id != 0:
            pass