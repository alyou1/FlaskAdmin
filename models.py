from extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(40))
    is_super_user = db.Column(db.String(40))

    def __init__(self, username,name,password,is_super_user):
        self.username = username
        self.name = name
        self.password = password
        self.is_super_user = is_super_user

