from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from django.utils import timezone
import logging

from network.models import User, Postings, Followings, Likes

class BrowserFollowingsTestCase(StaticLiveServerTestCase):
    """
    Test Followings Page functionality
    """
    test_browser = "Chrome"
    tester = "sekar"
    tester_password = "password"
    post_setup_count = 0
    browser = ""
    test_browser = ""
    logged_in_user = ""
    
    post = [
            ["sekar","Posting 1"],
            ["john", "Posting 2"],
            ["tim",  "Posting 3"],
            ["tim",  "Posting 4"],
            ["jane", "Posting 5"],
            ["jane", "Posting 6"],
            ["jane", "Posting 7"],
            ]
    
    post_setup_count = len(post)
    
    def setUp(self):
        """
        Setup the webdriver
        Setup 5 users
        """

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.set_window_size(1496, 875)
        self.test_browser = self.browser.capabilities['browserName']
        #print(f"window size: {self.browser.get_window_size()}")

        
        sekar = User.objects.create( username = self.tester, 
                                     is_superuser = False,
                                     is_staff = False,
                                     is_active = True,
                                     first_name = "Sekar",
                                     last_name = "Nagappan",
                                     email = "sekar@mail.com",
                                     date_joined = timezone.now(),
                                     followers_count = 0,
                                     followings_count = 0
                                     )
        sekar.set_password(self.tester_password)
        sekar.save()

        john = User.objects.create( username = 'john', 
                                    is_superuser = False,
                                    is_staff = False,
                                    is_active = True,
                                    first_name = "John",
                                    last_name = "Johns",
                                    email = "john@mail.com",
                                    date_joined = timezone.now(),
                                    followers_count = 0,
                                    followings_count = 0
                                    )
        john.set_password(self.tester_password)
        john.save()
      
        ann = User.objects.create( username = 'ann', 
                                   is_superuser = False,
                                   is_staff = False,
                                   is_active = True,
                                   first_name = "Ann",
                                   last_name = "Annie",
                                   email = "ann@mail.com",
                                   date_joined = timezone.now(),
                                   followers_count = 0,
                                   followings_count = 0
                                   )  
        ann.set_password(self.tester_password)
        ann.save()

        tim = User.objects.create( username = 'tim', 
                                   is_superuser = False,
                                   is_staff = False,
                                   is_active = True,
                                   first_name = "Tim",
                                   last_name = "Tom",
                                   email = "ann@mail.com",
                                   date_joined = timezone.now(),
                                   followers_count = 0,
                                   followings_count = 0
                                   )  
        tim.set_password(self.tester_password)
        tim.save()

        jane = User.objects.create( username = 'jane', 
                                   is_superuser = False,
                                   is_staff = False,
                                   is_active = True,
                                   first_name = "Jane",
                                   last_name = "Janny",
                                   email = "ann@mail.com",
                                   date_joined = timezone.now(),
                                   followers_count = 0,
                                   followings_count = 0
                                   )  
        jane.set_password(self.tester_password)
        jane.save()

        #Reduce the log level warning to avoid expected errors like 'not found
        logger = logging.getLogger("django.request")
        logger.setLevel(logging.ERROR)
        
        self.logged_in_user = self.login(self.tester, self.tester_password)

    def login(self, user, passw):

        browser = self.browser

        browser.get(f"{self.live_server_url}/login")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "login_button")))

        username = browser.find_element(By.NAME, "username")
        password = browser.find_element(By.NAME, "password")
        login_button = browser.find_element(By.ID, "login_button")

        username.clear()
        username.send_keys(user)
        password.clear()
        password.send_keys(passw)
        login_button.click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))
        heading = browser.find_element(By.ID, "newpost-h5").text
        self.assertEqual(heading, "All Posts", "Check you are on the index with the default all post section")
        self.logged_in_user = browser.find_element(By.ID, "username-nav").text
        self.assertEqual(user, self.logged_in_user, "Check the username on the nav bar is the user requested.")

        return self.logged_in_user

    def logout(self):

        browser = self.browser

        browser.find_element(By.ID, "logout-nav").click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "login-h2")))
        self.assertEqual(browser.find_element(By.ID, "login-h2").text, "Login", "Check you are on the login page")

    def postings(self):
        """
        Make a set of posting to be used later for testing paging.
        Ensure all posting get a successful response.
        """
        
        browser = self.browser
                
        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        for usr in ['sekar', 'john', 'ann', 'tim', 'jane']:
            if usr != self.logged_in_user:
                #print (f"Logging in : {usr}")
                self.logout()
                self.login(usr, self.tester_password)
                logged_in_usr = usr

            for p in self.post:
                if usr == p[0]:
                    post_box = browser.find_element(By.ID, "postings-body")
                    post_button = browser.find_element(By.ID, "posting-button")

                    post_box.send_keys(p[1])
                    post_button.click()
                    WebDriverWait(browser, 5, poll_frequency=0.5).until(EC.alert_is_present(), 'Response Message: Posting Done.')
                    alert = Alert(browser)
                    #print(alert.text)
                    post_msg = alert.text
                    self.assertEqual(alert.text[0:31], "Response Message: Posting Done.", "Check the Response message on the alert")

                    alert.accept()
                    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

                    post_id = int(post_msg.split(':')[2])
                    p.append(post_id)


    def test_followings(self):
        """
        Test followings view.
        Please note, we have already tested the follow and unfollow buttons in the profile view test.
        Here will set one user to follow a fw others and check the all post for the user we follow are displayed in the followings view.
        """
        self.postings()
                
        browser = self.browser

        self.logged_in_user = self.login(self.tester, self.tester_password)

        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        post_count = int(browser.find_element(By.ID, "post-count").text)
        self.assertEqual(post_count, len(self.post), "Check if there 7 post altogether")
        
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertGreaterEqual(len(posting_blocks), 7, "Check there are more then 5 posting on this page")
        
        post_id = int(posting_blocks[0].get_attribute('data-postblock')) #Should be Jane's Post
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        
        profile_user = posting_blocks[0].find_element(By.ID, f"post-user-{post_id}")
        
        profile_user.click() #Click on Jane's profile link and ensure the profile view is displayed.
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "profile-view")))
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "follow-button")))
        
        profile_id = browser.find_element(By.ID, "profile-id").text
        self.assertEqual(profile_id, 'jane', "Check if the profile shown is for Jane")
        
        #ensure the follow button is visible.
        follow_button = browser.find_element(By.ID, "follow-button")
        self.assertTrue(follow_button.is_displayed(), "check if the follow button is displayed.")
        self.assertTrue(follow_button.is_enabled(), "check if follow the button is enabled.")
                
        follow_button.click() #Click follow
        
        #back to index page.
        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))        
        
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        
        post_id = int(posting_blocks[3].get_attribute('data-postblock')) #Should be tim's Post
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view

        
        profile_user = posting_blocks[3].find_element(By.ID, f"post-user-{post_id}")
        #WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "post-user-{post_id}")))

        profile_user.click() #Click on Tims's profile link and ensure the profile view is displayed.
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "profile-view")))
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "follow-button")))
        
        profile_id = browser.find_element(By.ID, "profile-id").text
        self.assertEqual(profile_id, 'tim', "Check if the profile shown is for Jane")
        
        #ensure the follow button is visible.
        follow_button = browser.find_element(By.ID, "follow-button")
        self.assertTrue(follow_button.is_displayed(), "check if the follow button is displayed.")
        self.assertTrue(follow_button.is_enabled(), "check if follow the button is enabled.")
                
        follow_button.click() #Click follow
        
        followings_nav = browser.find_element(By.ID, "followings-nav")
        followings_nav.click()
        
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "followings-view")))
        post_count = int(browser.find_element(By.ID, "post-count").text)
        self.assertGreaterEqual(post_count, 5, "Check there are are 5 post that is being followed")
        
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertGreaterEqual(len(posting_blocks), 5, "Check there are 5 posting that are being followed")

        prev_post_ts = 0
        
        #For all the post on the profile-view, ensure all are Jane's and sorting order is correct.
        for posting in posting_blocks:
            post_id = int(posting.get_attribute('data-postblock'))
            post_user_id = browser.find_element(By.ID, f"post-user-{post_id}").text
            self.assertIn(post_user_id, ['jane', 'tim'], "Check if the poster is eiter Jane or tim")
            post_ts = int(browser.find_element(By.ID, f"post-ts-u-{ post_id }").get_attribute("textContent"))
            if prev_post_ts == 0:
                prev_post_ts = post_ts
            self.assertGreaterEqual(prev_post_ts, post_ts, "Check timestamp order")

                