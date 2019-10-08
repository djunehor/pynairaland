"""Browser Module"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

class Browser:
    """Browser class"""

    def __init__(self, linux):
        # Options for windows
        OPTION = Options()

        OPTION.add_argument("--disable-infobars")
        OPTION.add_argument("start-maximized")
        OPTION.add_argument("--disable-extensions")
        OPTION.add_argument("--headless")
        # disable notifications popup alert
        OPTION.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
        )

        # specifies the path to the chromedriver.exe
        CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '/usr/bin/chromedriver')
        GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', os.getcwd()+'\driver\\chromedriver.exe')
        GOOGLE_CHROME_PATH = os.getcwd()+'\driver\\chromedriver.exe'

        # Options for LINUX
        options = Options()
        options.binary_location = GOOGLE_CHROME_BIN
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        if linux == 'True':
            self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
        else:
            self.driver = webdriver.Chrome(executable_path=GOOGLE_CHROME_PATH, options=OPTION)

    def get_url(self, url):
        """Navigates to URL"""
        self.driver.get(url)
        # print("[Browser] Visited ", url)

    def login(self, username, user_pass):
        self.driver.get('https://www.nairaland.com/login')

        # locate email form by_class_name
        user_name = self.driver.find_element_by_xpath("//input[@name='name']")

        # send_keys() to simulate key strokes
        user_name.send_keys(username)

        password = self.driver.find_element_by_xpath("//input[@name='password']")
        password.send_keys(user_pass)
        self.driver.find_element_by_xpath("//input[@value='Login']").click()
        time.sleep(1)
        self.driver.get(self.driver.current_url)
        if 'Nairaland Forum' in self.driver.page_source:
            print('Logged in as ', username)
            return True
        else:
            print('Login failed: ', self.driver.title)
            return False

    def get_source(self):
        """Returns current page source html"""
        return self.driver.page_source.encode('utf-8')

    def resolve_category(self, name):

        '''
        Get a key from dictionary which has the given value
        '''

    def get_key_by_value(self, value_to_find):
        dict_of_elements = {
        "0": "-- All Sections --",
        "32": "Adverts",
        "85": "Agriculture",
        "45": "Art, Graphics & Video",
        "26": "Autos",
        "24": "Business",
        "49": "Business To Business",
        "78": "Car Talk",
        "35": "Career",
        "46": "Celebrities",
        "62": "Certification And Training Adverts",
        "74": "Computer Market",
        "22": "Computers",
        "1": "Crime",
        "55": "Culture",
        "38": "Dating And Meet-up Zone",
        "31": "Diaries",
        "13": "Education",
        "57": "Educational Services",
        "12": "Entertainment",
        "40": "Ethnic, Racial, Or Sectarian Politics",
        "66": "European Football (EPL, UEFA, La Liga)",
        "7": "Events",
        "5": "Family",
        "37": "Fashion",
        "39": "Fashion/Clothing Market",
        "41": "Food",
        "61": "Foreign Affairs",
        "33": "Forum Games",
        "10": "Gaming",
        "51": "Graphics/Video Market",
        "19": "Health",
        "23": "Home Page",
        "81": "Investment",
        "82": "Investment Ads",
        "44": "Islam for Muslims",
        "29": "Jobs/Vacancies",
        "15": "Jokes Etc",
        "11": "Literature",
        "42": "Literature/Writing Ads",
        "65": "Moderators",
        "59": "Music Business",
        "3": "Music/Radio",
        "9": "Nairaland / General",
        "80": "Nairaland Ads",
        "79": "NYSC",
        "84": "Pets",
        "75": "Phone/Internet Market",
        "16": "Phones",
        "36": "Poems For Review",
        "20": "Politics",
        "34": "Programming",
        "47": "Properties",
        "60": "Rap Battles",
        "53": "Recycle Bin",
        "17": "Religion",
        "21": "Romance",
        "58": "Satellite TV Technology",
        "8": "Science/Technology",
        "28": "Sexuality",
        "76": "Software/Programmer Market",
        "14": "Sports",
        "54": "Technology Market",
        "83": "Top Pages",
        "2": "Travel",
        "77": "Travel Ads",
        "4": "TV/Movies",
        "71": "Video Games And Gadgets For Sale",
        "52": "Web Market",
        "30": "Webmasters",
        }
        key = None

        list_of_items = dict_of_elements.items()
        for item in list_of_items:
            if item[1] == value_to_find:
                key = item[0]
        return key
