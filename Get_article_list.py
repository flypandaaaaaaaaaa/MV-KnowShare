from MySQL_Modules import article,del_article

class Get_article(object):
    def __init__(self,PageID=7,limitation=5,Only_PB='Y'):
        self.PageID=PageID
        self.limitation=limitation
        self.Only_PB=Only_PB
    def Get_all_article_desc_date(self):
        Article_all_list = article.query.filter(article.read_public==self.Only_PB).order_by(article.created_date.desc())
        return Article_all_list
    def Get_article_page_list_desc_id(self):
        Article_list = article.query.filter(article.read_public==self.Only_PB).filter(article.id.in_(self.PageID)).order_by(article.id.desc())
        return Article_list
    def Get_article_list_recent_desc(self):
        Article_list_recent = article.query.filter(article.read_public==self.Only_PB).order_by(article.created_date.desc()).limit(self.limitation).offset(0)
        return Article_list_recent
    def Get_article_list_most_desc(self):
        Article_list_most = article.query.filter(article.read_public==self.Only_PB).order_by(article.read_num.desc()).limit(self.limitation).offset(0)
        return Article_list_most

    def Get_all_del_article_desc_date(self):
        Article_all_list = del_article.query.order_by(del_article.created_date.desc())
        return Article_all_list
    def Get_del_article_page_list_desc_id(self):
        Article_list = del_article.query.filter(del_article.id.in_(self.PageID)).order_by(article.id.desc())
        return Article_list
    def Get_del_article_list_recent_desc(self):
        Article_list_recent = del_article.query.order_by(del_article.created_date.desc()).limit(self.limitation).offset(0)
        return Article_list_recent
    def Get_del_article_list_most_desc(self):
        Article_list_most = del_article.query.order_by(del_article.read_num.desc()).limit(self.limitation).offset(0)
        return Article_list_most