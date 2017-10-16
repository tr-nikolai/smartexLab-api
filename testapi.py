from app import app
import unittest
import json


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.last_name = 'TestLastName'
        self.first_name = 'TestFirstName'
        self.patronymic_name = 'TestPalName'
        self.password = 'TestPassword'
        self.email = 'TestEmail@gmail.com'
        self.fake_password = 'TestPassword123'

    def test_a_post_create_user(self):
        response = self.app.post('/users', data=json.dumps(dict(
            last_name=self.last_name,
            first_name=self.first_name,
            patronymic_name=self.patronymic_name,
            password=self.password,
            email=self.email)), follow_redirects=False, content_type='application/json')
        decode_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertIn('User created:', decode_data['message'])

    def test_b_get_all_users(self):
        response = self.app.get('/users')
        tmp_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertIsNotNone(tmp_data['users'])

    def test_c_get_one_user(self):
        response = self.app.get('/users')
        tmp_data = json.loads(response.data.decode('utf-8'))
        user = tmp_data['users'][0]
        response_user = self.app.get('/users/' + str(user['id']))
        tmp_data_user = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(response_user.mimetype, 'application/json')
        self.assertIsNotNone(tmp_data_user)

    def test_d_get_one_user_not_found(self):
        response = self.app.get('/users/1000000')
        tmp_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual('User not found!', tmp_data['error'])

    def test_e_post_user_not_created(self):
        response = self.app.post('/users', data=json.dumps(dict(
            last_name=self.last_name,
            first_name=self.first_name,
            patronymic_name=self.patronymic_name,
            email=self.email, )), follow_redirects=False, content_type='application/json')
        decode_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertIn('User not created - Invalid names or number of columns.', decode_data['error'])

    def test_f_post_user_not_created_empty(self):
        response = self.app.post('/users', data=json.dumps(dict(
            last_name="",
            first_name="",
            patronymic_name="",
            password="",
            email="", )), follow_redirects=False, content_type='application/json')
        decode_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertIn('User not created - columns should not be empty', decode_data['error'])

    def test_g_created_card(self):
        response = self.app.get('/users')
        tmp_data = json.loads(response.data.decode('utf-8'))
        last_created_user = tmp_data['users'][-1]
        if last_created_user['first_name'] == self.first_name:
            user_id = last_created_user['id']
            response_card = self.app.post('/users/' + str(user_id) + '/cards',
                                          data=json.dumps(dict(password=self.password)),
                                          follow_redirects=False, content_type='application/json')
            tmp_data_card = json.loads(response_card.data.decode('utf-8'))
            self.assertEqual(response_card.status_code, 200)
            self.assertEqual(response_card.mimetype, 'application/json')
            self.assertIn('created', tmp_data_card['message'])

    def test_h_not_created_card_(self):
        response = self.app.get('/users')
        tmp_data = json.loads(response.data.decode('utf-8'))
        last_created_user = tmp_data['users'][-1]
        if last_created_user['first_name'] == 'TestFitstName':
            user_id = last_created_user['id']
            response_card = self.app.post('/users/' + str(user_id) + '/cards',
                                          data=json.dumps(dict(password=self.fake_password)),
                                          follow_redirects=False, content_type='application/json')
            tmp_data_card = json.loads(response_card.data.decode('utf-8'))
            self.assertEqual(response_card.status_code, 400)
            self.assertEqual(response_card.mimetype, 'application/json')
            self.assertIn('Password is not valid!', tmp_data_card['error'])

    def test_i_not_created_card_not_found(self):
        response_card = self.app.post('/users/100000/cards',
                                      data=json.dumps(dict(password=self.fake_password)),
                                      follow_redirects=False, content_type='application/json')
        tmp_data_card = json.loads(response_card.data.decode('utf-8'))
        self.assertEqual(response_card.status_code, 404)
        self.assertEqual(response_card.mimetype, 'application/json')
        self.assertIn('User not found!', tmp_data_card['error'])

    def test_j_delete_user_not_found(self):
        response_user = self.app.delete('/users/1000000',
                                        data=json.dumps(dict(password=self.fake_password)),
                                        follow_redirects=False, content_type='application/json')
        tmp_data_user = json.loads(response_user.data.decode('utf-8'))
        self.assertEqual(response_user.status_code, 404)
        self.assertEqual(response_user.mimetype, 'application/json')
        self.assertIn('User not found!', tmp_data_user['error'])

    def test_k_delete_user_check_password(self):
        response = self.app.get('/users')
        tmp_data = json.loads(response.data.decode('utf-8'))
        list_users = tmp_data['users']
        count = 0
        for user in list_users:
            if user['email'] == self.email:
                last_created_user = tmp_data['users'][count]
                user_id = last_created_user['id']
                response_user = self.app.delete('/users/' + str(user_id),
                                                data=json.dumps(dict(password=self.fake_password)),
                                                follow_redirects=False, content_type='application/json')
                tmp_data_user = json.loads(response_user.data.decode('utf-8'))
                self.assertEqual(response_user.status_code, 400)
                self.assertEqual(response_user.mimetype, 'application/json')
                self.assertIn('Password is not valid!!', tmp_data_user['error'])

    def test_l_delete_user(self):
        response = self.app.get('/users')
        tmp_data = json.loads(response.data.decode('utf-8'))
        list_users = tmp_data['users']
        count = 0
        for user in list_users:
            if user['email'] == self.email:
                last_created_user = tmp_data['users'][count]
                user_id = last_created_user['id']
                response_user = self.app.delete('/users/' + str(user_id),
                                                data=json.dumps(dict(password=self.password)),
                                                follow_redirects=False, content_type='application/json')
                tmp_data_user = json.loads(response_user.data.decode('utf-8'))
                self.assertEqual(response_user.status_code, 200)
                self.assertEqual(response_user.mimetype, 'application/json')
                self.assertIn('User deleted:', tmp_data_user['message'])


if __name__ == '__main__':
    unittest.main()
