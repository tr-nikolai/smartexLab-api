from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'smaertexlab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/nikolai/PycharmProjects/smartexlab/test.db'
db = SQLAlchemy(app)
admin = Admin(app, name='smartexLab', template_mode='bootstrap3')


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.Unicode, nullable=False)
    first_name = db.Column(db.Unicode, nullable=False)
    patronymic_name = db.Column(db.Unicode, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Unicode)


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(13), unique=True, )
    cvv_code = db.Column(db.Unicode, nullable=False)
    pin_code = db.Column(db.Unicode, nullable=False)
    validity_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users, backref=db.backref('cards', lazy='dynamic', cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Cards %r>' % self.number


@app.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'last_name': user.last_name, 'first_name': user.first_name,
                     'patronymic_name': user.first_name, 'password': user.password, 'email': user.email,
                     'user_cards': 'users/' + str(user.id) + '/cards'}
        output.append(user_data)
    return jsonify({'users': output})


@app.route('/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message':'User not found!'})
    user_data = {'id': user.id, 'last_name': user.last_name, 'first_name': user.first_name,
                 'patronymic_name': user.first_name, 'password': user.password, 'email': user.email,
                 'user_cards':'users/'+ str(user.id) +'/cards'}
    return jsonify(user_data)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Users(last_name=data['last_name'], first_name=data['first_name'], patronymic_name=data['patronymic_name'],
                     password=hashed_password, email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created'})


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User has been deleted!'})


#блок для карт
@app.route('/users/<user_id>/cards', methods=['GET'])
def get_user_cards(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message':'User not found!'})
    cards = Cards.query.filter_by(user_id=user_id)
    output = []
    for card in cards:
        card_data = {'number': card.number, 'cvv_code': card.cvv_code, 'pin_code':card.pin_code,
                     'user_id':card.user_id,'validity_date': card.validity_date}
        output.append(card_data)
    return jsonify({'cards': output})


@app.route('/cards', methods=['GET'])
def get_all_cards():
    cards = Cards.query.all()
    output = []
    for card in cards:
        card_data = {'number': card.number, 'cvv_code': card.cvv_code, 'pin_code':card.pin_code,
                     'user_id':card.user_id,'validity_date': card.validity_date}
        output.append(card_data)
    return jsonify({'cards': output})

def generate_new_card():
    list_number = []
    while len(list_number) != 13:
        list_number.append(str(randint(0, 9)))
    number_new_card = ''.join(list_number)
    list_cvv = []
    while len(list_cvv) != 3:
        list_cvv.append(str(randint(0, 9)))
    cvv_new_card = ''.join(list_cvv)
    list_pin = []
    while len(list_pin) != 4:
        list_pin.append(str(randint(0, 9)))
    pin_new_card = ''.join(list_number)
    return number_new_card,  cvv_new_card, pin_new_card


@app.route('/users/<user_id>/cards', methods=['POST'])
def create_user_card(user_id):
    user = Users.query.filter_by(id=user_id).first()
    data = request.get_json()
    if not user:
         return jsonify({'message':'User not found!'})
    if check_password_hash(user.password, data['password']):
        number_new_card, cvv_new_card, pin_new_card  = generate_new_card()
        hashed_cvv = generate_password_hash(cvv_new_card, method='sha256')
        hashed_pin = generate_password_hash(pin_new_card, method='sha256')
        validadion_date = datetime.now() + timedelta(days=365)
        new_card = Cards(number=number_new_card, cvv_code=hashed_cvv, pin_code=hashed_pin, user_id=user_id,
                         validity_date=validadion_date )
        db.session.add(new_card)
        db.session.commit()
        return jsonify({'message': 'New card created!'})
    else:
        return jsonify({'message': 'Password is not valid!'})




db.create_all()


class UsersModelView(ModelView):
    # can_delete = False
    # can_create = False
    # can_edit = False
    column_list = ('id', 'last_name', 'first_name', 'patronymic_name', 'password', 'email')
    column_labels = dict(id='id', last_name='Фамилия', first_name='Имя', patronymic_name='Отчество', password='пароль',
                         email='email')
    page_size = 20  # the number of entries to display on the list view


class CardsModelView(ModelView):
    # can_delete = False
    # can_create = False
    # can_edit = False
    page_size = 20  # the number of entries to display on the list view


admin.add_view(UsersModelView(Users, db.session))
admin.add_view(CardsModelView(Cards, db.session))

# admin.add_view(ModelView(Users, db.session))
# admin.add_view(ModelView(Cards, db.session))

# boby = Users.query.all()
# start the flask loop
if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', debug=True, port=12337, use_reloader=True)
