import unittest
import os
from dotenv import load_dotenv

from nairaland import Nairaland
from nairaland import User
from nairaland.browser import Browser


class TestCase(unittest.TestCase):
    def setUp(self):
        load_dotenv('.env')
        self.browser = Browser(os.environ.get('LINUX'))
        self.nairaland = Nairaland(self.browser)
        self.user = User(self.browser)
        self.category = 'politics'
        self.topic = '5460114'
        self.search = 'buhari'
        self.username = os.environ.get('NL_USERNAME')
        self.password = os.environ.get('NL_PASSWORD')
        self.logged_in = self.browser.login(self.username, self.password)

    def tearDown(self):
        self.browser.driver.quit()

    def test_front_page_topics(self):      
        assert type(self.nairaland.front_page_topics()) == dict

    def test_categories(self):      
        assert type(self.nairaland.categories()) == dict

    def test_trending_topics(self):      
        assert type(self.nairaland.trending_topics()) == dict

    def test_new_topics(self):      
        assert type(self.nairaland.new_topics()) == dict

    def test_recent_posts(self):      
        assert type(self.nairaland.recent_posts()) == dict

    def test_user(self):      
        assert type(self.nairaland.user(self.username)) == dict

    def test_user_posts(self):      
        assert type(self.nairaland.user_posts(self.username)) == dict

    def test_user_topics(self):      
        assert type(self.nairaland.user_topics(self.username)) == dict

    def test_category_topics(self):      
        assert type(self.nairaland.category_topics(self.category)) == dict

    def test_topic_posts(self):      
        assert type(self.nairaland.topic_posts(self.topic)) == dict

    def test_search(self):      
        assert type(self.nairaland.search(self.search)) == dict

    def test_login(self): 
        if not self.logged_in:
            assert self.browser.login(self.username, self.password) == True
        else:
            assert self.logged_in == True

# Authenticated methods
    def test_user_followed_topics(self):
        assert type(self.user.followed_topics()) == dict

    def test_user_followed_boards(self):
        assert type(self.user.followed_boards()) == dict

    def test_user_likes_and_shares(self):
        assert type(self.user.likes_and_shares()) == dict

    def test_user_mentions(self):
        assert type(self.user.mentions()) == dict

    def test_user_following_posts(self):
        assert type(self.user.following_posts()) == dict

    def test_user_shared_with(self):
        assert type(self.user.shared_with()) == dict


if __name__ == "__main__":
    unittest.main()