from flask import url_for
from application import app, db
from application.models import *
from flask_testing import TestCase
from datetime import date, timedelta


class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test-app.db',
            WTF_CSRF_ENABLED = False,
            DEBUG = True,
            SECRET_KEY ='SASASASA'
        )

        return app


    def setUp(self): # Runs before each test
        db.create_all()
        user1 = User(first_name = 'Sample', last_name = 'Gurung')
        review1 = Review(book = 'Sample Book', book_review = 'Excellent', review_date = date.today()+ timedelta(30), review_by = 'Kevin')
        db.session.add(user1)
        db.session.add(review1)
        db.session.commit()


    def tearDown(self): #runs after every test
        db.session.remove()
        db.drop_all()


class TestHomeView(TestBase):
    def test_get_home(self):
        response = self.client.get(url_for('index'))
        self.assert200(response)
        self.assertIn(b'Book Review', response.data) 

    def test_get_users(self):
        response = self.client.get(url_for('view_all_users'))
        self.assert200(response)
        self.assertIn(b'Sample, Gurung', response.data)

    def test_get_reviews(self):
        response = self.client.get(url_for('view_all_reviews'))
        self.assert200(response)
        self.assertIn(b'Sample Book', response.data)
        
    
    def test_get_add_u(self):
        response = self.client.get(url_for('add_user'))
        self.assert200(response)
        self.assertIn(b'First Name', response.data)
    
    def test_get_add_r(self):
        response = self.client.get(url_for('create_new_review'))
        self.assert200(response)
        self.assertIn(b'Book', response.data)
    
    def test_get_update_u(self):
        response = self.client.get(url_for('update_user', id=1))
        self.assert200(response)
        self.assertIn(b'First Name', response.data)

    def test_get_update_r(self):
        response = self.client.get(url_for('update_user', id=1))
        self.assert200(response)
        self.assertIn(b'Book', response.data)
    
    def test_get_delete_u(self):
        response = self.client.get(
            url_for('delete_user', id=1),
            follow_redirects = True
        )
        self.assert200(response)
        self.assertNotIn(b'Sample, Gurung', response.data)

    def test_get_delete_r(self):
        response = self.client.get(
            url_for('delete_review', id=1),
            follow_redirects = True
        )
        self.assert200(response)
        self.assertNotIn(b'Sample Book', response.data)

class TestPostRequests(TestBase):
    def test_post_add_u(self):
        response = self.client.post(
            url_for('add_user'),
            data = dict(first_name = 'King', last_name = 'JJ'),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'King, JJ', response.data)
    

    def test_post_update_u(self):
        response = self.client.post(
            url_for('update_user', id=1),
            data = dict(first_name='New', last_name='Data'),
            follow_redirects=True
        )

        self.assert200(response)
        assert User.query.filter_by(first_name='New').first() is not None
        assert User.query.filter_by(first_name='Sample').first() is None


    def test_post_add_r(self):
        response = self.client.post(
            url_for('create_new_review'),
            data = dict(
                book = 'Another Book Sample', 
                book_review='Yet another sample task',  
                review_date = date.today() + timedelta(30), 
                review_by=1
                ),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Another Book Sample', response.data)



    def test_post_update_r(self):
        response = self.client.post(
            url_for('update_review', id=1),
            data = dict(
                book ='Updated Name',
                book_review ='New rev',
                review_date = date.today() + timedelta(14), 
                review_by=1
                ),
            follow_redirects = True
        )
        self.assert200(response)
        
        