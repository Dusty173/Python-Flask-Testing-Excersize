from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set up before running tests"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        """Verify info is being displayed to page"""
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numplays'))


    def test_is_word(self):
        """Force board into word and verify its a valid word"""
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [
                                    ['A','P','P','L','E'],
                                    ['A','P','P','L','E'],
                                    ['A','P','P','L','E'],
                                    ['A','P','P','L','E'],
                                    ['A','P','P','L','E']
                                  ]
        res = self.client.get('/verify-word?word=apple')
        self.assertEqual(res.json['result'], 'ok')

    def test_bad_input(self):
        """Check dict for word that can't exist on board"""
        self.client.get('/')
        res = self.client.get('/verify-word?word=dictionary')
        self.assertEqual(res.json['result'], 'not-on-board')

    def test_not_word(self):
        """Check if word is real english"""
        self.client.get('/')
        res = self.client.get('/verify-word?word=wawaweewaaaa')
        self.assertEqual(res.json['result'], 'not-word')