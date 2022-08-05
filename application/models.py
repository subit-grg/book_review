from application import db

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key = True)
    book = db.Column(db.String(20))
    book_review = db.Column(db.String(50))
    review_date = db.Column(db.Date)
    review_by = db.Column(db.Integer, db.ForeignKey('user.uid'))
    def __str__(self):
        return f"{self.book}: {self.book_review}. Review date: {self.review_date}."

class User(db.Model):
    uid = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    reviews = db.relationship('Review', backref='user')
    def __str__(self):
        return f"{self.first_name}, {self.last_name}"