from flask import Flask, jsonify ,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# < >
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:airflow97@localhost/students"
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'mysecret'


db = SQLAlchemy(app)
ma = Marshmallow(app)

admin = Admin(app, name='Gestion des utilisateurs', template_mode='bootstrap3')

# Class Student
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

# Add administrative views here
with app.app_context():
    admin.add_view(ModelView(User,db.session()))

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id","username","name","password","is_super_user")

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)



@app.before_request
def before():
    print("This is executed BEFORE each request.")


# create users
@app.route('/api/users/',methods=['POST'])
def add_user():
    data = request.get_json()
    username = data['username']
    name = data['name']
    password = data['password']
    is_super_user = data['is_super_user']


    with app.app_context():
        db.create_all()
        user = User(username,name,password,is_super_user)
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user), 201 # created



# Get all users
@app.route('/api/users/',methods=['GET'])
def get_users():
    with app.app_context():
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result), 200

# Get single user
@app.route('/api/users/<id>',methods=['GET'])
def get_student(id):
    with app.app_context():
        user = User.query.get(id)
        return user_schema.jsonify(user), 200

# update a user
@app.route('/api/users/<id>',methods=['PUT'])
def update_student(id):
    with app.app_context():
        user = User.query.get(id)
        data = request.get_json()
        username = data['username']
        name = data['name']
        password = data['password']
        is_super_user = data['is_super_user']

        user.username = username
        user.name = name
        user.password = password
        user.is_super_user = is_super_user

        db.session.commit()
        return user_schema.jsonify(user), 201 # created


# delete user
@app.route('/api/users/<id>',methods=['DELETE'])
def delete_student(id):
    with app.app_context():
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)