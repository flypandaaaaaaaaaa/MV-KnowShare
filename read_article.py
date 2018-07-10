from MySQL_Modules import article,del_article
from mvknow_init import db
from flask_login import current_user

class read_my_article(object):

    def __init__(self,article_id):
        self.__article_id=article_id

    def read(self):

        if current_user.is_anonymous:
            Article=article.query.filter_by(id=self.__article_id).first()
            Article.read_num=Article.read_num+1
            db.session.commit
            return  Article

        else:
            Article = article.query.filter_by(id=self.__article_id).first()
            Del_Article = del_article.query.filter_by(id=self.__article_id).first()
            if Article is not None:
                return Article
            else:
                return Del_Article


