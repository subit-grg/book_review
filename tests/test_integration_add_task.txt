from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from application import app, db
from application.models import *
from application.forms import *
from datetime import date, timedelta

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test-app.db',
            LIVESERVER_PORT = self.TEST_PORT,
            DEBUG = True,
            TESTING = True
        )

        return app
    
    def setUp(self):
        db.create_all()
        sample_user = User(first_name="John", last_name="Smith")
        db.session.add(sample_user)
        db.session.commit()
        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f'http://localhost:{self.TEST_PORT}/add-review')

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
    
    def test_server_connectivity(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}/add-review')
        assert response.status == 200

class TestAddUser(TestBase):
    def submit_input(self, test_case, test_valid = False):
        book_field = self.driver.find_element_by_xpath('/html/body/div/form/input[2]')
        book_review_field = self.driver.find_element_by_xpath('/html/body/div/form/textarea')
        review_date_field = self.driver.find_element_by_xpath('/html/body/div/form/input[3]')
        review_by_field = self.driver.find_element_by_xpath('/html/body/div/form/select[2]')
        submit = self.driver.find_element_by_xpath('/html/body/div/form/input[4]')
        book_field.send_keys(test_case[0])
        book_review_field.send_keys(test_case[1])
        if test_valid:
            review_date_field.clear()
        review_by_field.send_keys(test_case[3])
        submit.click()
    
    def test_add_review(self):
        test_case = "Sample Review", "A review for the integration test", 'book review', 'JJ Smile'
        self.submit_input(test_case)
        assert list(Review.query.all()) != []
        assert Review.query.filter_by(book="Sample Review").first() is not None

    def test_add_review_validation(self):
        test_case = "Sample Review", "A review for the integration test", 'book review', 'Jyle Smith'
        self.submit_input(test_case, test_valid=True)
        assert list(Review.query.all()) == []
        assert Review.query.filter_by(book="Sample Review").first() is None
