import unittest
from app import create_app
import logging
import pprint
from flask import session



class SongTestCase(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(levelname)s %(filename)s %(funcName)s %(lineno)d : %(message)s \n\n'
    )

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True


    @unittest.skip("too dum")
    def test_get_song(self):
        response = self.app.get('/songs/0AqhwhQv1xnqCH9wzlQ7PE/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["SONG_NAME"], "Stronger")

    # endpoint for getting a list of songs that match the given hints after user makes a guess
    def test_get_guess_list(self):
        response = self.app.post('/songs/similarlist/',
                                json= {'hints': {'acousticness': {'known': False, 'value': 0.0295},
           'album': {'known': False,
                     'name': 'Unreal Unearth: Unheard',
                     'value': '1vL2mgGTukkrUxXt0loeTN'},
           'artists': [{'genres': [{'known': False, 'value': 'folk'}],
                        'known': False,
                        'name': 'Hozier',
                        'value': '2FXC3k01G6Gw61bmprjgqS'}],
           'danceability': {'known': False, 'value': 0.741},
           'energy': {'known': False, 'value': 0.62},
           'instrumentalness': {'known': False, 'value': 0.000809},
           'liveness': {'known': False, 'value': 0.0398},
           'loudness': {'known': False, 'value': -5.505},
           'mode': {'known': False, 'value': 1},
           'releasedate': {'known': False, 'value': '03-22-2024'},
           'speechiness': {'known': False, 'value': 0.0412},
           'tempo': {'known': False, 'value': 117.038},
           'title': {'known': False, 'value': 'Too Sweet'},
           'valence': {'known': False, 'value': 0.934}},
 'text': 'Du'})
        print(response.json)
        formatted_json = pprint.pformat(response.json)
        # print(formatted_json)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

    # endpoint for querying from cache built in get_guess_list when user changes input
    # this should prob be in puzzle module
    # def test_get_list_from_cache(self):
    #     response = self.app.get('/songs/36/36jvZGzkha6Iofib8BBzOL/48/1')
    #     formatted_json = pprint.pformat(response.json)
    #     print(formatted_json)
    #     self.assertEqual(response.status_code, 200)

    




if __name__ == '__main__':
    unittest.main()
