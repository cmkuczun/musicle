from typing import Any, NoReturn
import unittest
from app import create_app
import datetime

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    # def test_create_user(self):
    #     payload = {'username': 'test_user', 'password': 'test_password'}
    #     response = self.app.post('/users/', json=payload)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json, {"message": "User Added to Database"})

    # def test_login(self):
    #     payload = {'username': 'test_user', 'password': 'test_password'}
    #     response = self.app.post('/users/login/', json=payload)
    #     print(response.json)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(response.json)

    # def test_bad_login(self):
    #     payload = {'username': 'test_user', 'password': 'wrong_password'}
    #     response = self.app.post('/users/login/', json=payload)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json, {"message": "User Not Found"})

    # def test_post_data_failure(self):
    #     response = self.app.post('/users/', json={})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json, {'error': 'No Data Provided'})

    # def test_get_users(self):
    #     response = self.app.get('/users/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(response.json)

    @unittest.skip("too dum")
    def test_get_user(self):
        response = self.app.get('/users/33/')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json,
        #                  {'USERNAME': 'TESTCRTUSER2',
        #                   'PASSWORD': 'TESTCRTPASS2',
        #                   'USER_ID': 1})

    @unittest.skip("too dum")
    def test_get_user_stats(self):
        response = self.app.get('/users/48/stats/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)

    # def test_get_global_stats(self):
    #     response = self.app.get('/users/stats/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(response.json)
    #     print("Stats for all users: ", response.json)

    @unittest.skip("too dum")
    def test_get_user_stats_failure(self):
        response = self.app.get('/users/99999/stats/')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'user_stats': None, 'global_stats': None})

    @unittest.skip("too dum")
    def test_get_past_guesses(self):
        response = self.app.get('/users/48/36/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)

    def test_user_guess(self):
        payload = self.app.get('/users/config/5Z0UnEtpLDQyYlWwgi8m9C/') ## get sample "answer" config
        print(payload)
        response = self.app.post('/users/34/174/5QRJil6wshVx4Hy82yQvSs/1/', json=payload.json) # the user's guess config
        print("\nSENDING GUESS AND GETTING:\n")
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)

    def test_create_user_puzzle(self):
        payload = {
            "minYear" : "2019",
            "maxYear" : "2022",
            "genres" : ["pop", "turkish"]
        }
        response = self.app.post('/users/puzzle/48/', json=payload)
        print('PUZZLE CREATED FROM USER', response.json)

        self.assertEqual(response.status_code, 200)


    def test_puzzle_from_date(self):
        response = self.app.get('/users/puzzle/2024-05-02/')
        print("PUZZLE FROM DATE", response.json)
        self.assertEqual(response.status_code, 200)


        



if __name__ == '__main__':
    unittest.main()
