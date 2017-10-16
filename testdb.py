import unittest
from app import db, Users, Cards
from utils import generate_new_card
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta


class UsersTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDrop(self):
        db.session.remove()
        db.drop_all()

    def test_1_create_user(self):
        db.session.add(Users(last_name='Test', first_name='Test1', patronymic_name='Test2',
                             password='Test3', email='test@test.com'))
        db.session.commit()
        user = Users.query.filter_by(email='test@test.com').first()
        self.assertEqual('test@test.com', user.email)

    def test_2_create_card(self):
        user = db.session.query(Users).filter(Users.email == 'test@test.com').first()
        number_new_card, cvv_new_card, pin_new_card = generate_new_card()
        hashed_cvv = generate_password_hash(cvv_new_card, method='sha256')
        hashed_pin = generate_password_hash(pin_new_card, method='sha256')
        val_date = datetime.now() + timedelta(days=365)
        new_card = Cards(number=number_new_card,
                         cvv_code=hashed_cvv,
                         pin_code=hashed_pin,
                         user_id=user.id,
                         validity_date=val_date)
        db.session.add(new_card)
        db.session.commit()
        card = db.session.query(Cards).filter(Cards.user_id == user.id).first()
        self.assertIsNotNone(card)

    def test_3_delete_user(self):
        user = db.session.query(Users).filter(Users.email == 'test@test.com').first()
        db.session.delete(user)
        db.session.commit()
        self.assertIsNone(db.session.query(Users).filter(Users.email == 'test@test.com').first())

    def test_4_check_cards_deleted(self):
        user = db.session.query(Users).filter(Users.email == 'test@test.com').first()
        try:
            card = db.session.query(Cards).filter(Cards.user_id == user.id).first()
        except:
            card = None
        self.assertIsNone(card)


if __name__ == '__main__':
    unittest.main()
