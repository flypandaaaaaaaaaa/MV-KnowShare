from mvknow_init import db
class article(db.Model):
    __tablename__='article'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.String(10000))
    created_date=db.Column(db.Date)
    author=db.Column(db.String(100))
    read_num=db.Column(db.Integer)
    def __repr__(self):
        return '<article %r>' % self.title
