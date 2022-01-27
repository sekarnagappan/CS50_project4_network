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
from password_generator import PasswordGenerator

from network.models import User, Postings, Followings, Likes

class BrowserProfilesPageTestCase(StaticLiveServerTestCase):
    """
    Test Profile Page functionality.
    Navigate to the profiles page for a user and test follow/unfollow.
    """
    test_browser = ""
    tester = "sekar"
    pwo = PasswordGenerator()
    tester_password = pwo.generate()
    post_setup_count = 0
    test_browser = ""
    browser = ""
    logged_in_user = ""
    
    post = [
            ["sekar","Posting 1"],
            ["john", "Posting 2"],
            ["ann",  "Posting 3"],
            ["tim",  "Posting 4"],
            ["jane", "Posting 5"],
            ["sekar","Posting 6"],
            ["sekar","Posting 7"],
            ["john", "Posting 8"],
            ["john", "Posting 9"],
            ["ann",  "Posting 10"],
            ["ann",  "Posting 11"],
            ["jane", "Posting 12"],
            ["sekar","Posting 13"],
            ["john", "Posting 14"],
            ["ann",  "Posting 15"],
            ["tim",  "Posting 16"],
            ["jane", "Posting 17"],
            ["sekar","Posting 18"],
            ["sekar","Posting 19"],
            ["john", "Posting 20"],
            ["john", "Posting 21"]
            ]
    
    post_setup_count = len(post)
    
    def setUp(self):

        """
        Setup the webdriver
        Setup 5 user for the test
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

        ann = User.objects.create( username = 'tim', 
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
        ann.set_password(self.tester_password)
        ann.save()

        ann = User.objects.create( username = 'jane', 
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
        ann.set_password(self.tester_password)
        ann.save()

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
        Make a set of posting to be used later testing.
        Ensure all posting get a successful response.
        """
        
        browser = self.browser

        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        for usr in ['sekar', 'john', 'ann', 'tim', 'jane']:
            if usr != self.logged_in_user:
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
                    post_msg = alert.text
                    self.assertEqual(alert.text[0:31], "Response Message: Posting Done.", "Check the Response message on the alert")

                    alert.accept()
                    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

                    post_id = int(post_msg.split(':')[2])
                    p.append(post_id)
                    

    def test_profiles(self):
        """
        Test for the profile page.
        """

        self.postings()
        
        self.logged_in_user = self.login(self.tester, self.tester_password)        

        browser = self.browser
        wait = WebDriverWait(browser, 5, poll_frequency=0.25)
        
        #Ensure you are on the index, all post page.
        browser.get(f"{self.live_server_url}/index")
        wait.until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        #check there are 21 post and 10 items on this page.
        post_count = int(browser.find_element(By.ID, "post-count").text)
        self.assertEqual(post_count, len(self.post), "Check if there 21 post altogether")
        
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertEqual(len(posting_blocks), 10, "Check there are 10 posting on this page")

        #Choose the first post, should be Jane's
        post_id = int(posting_blocks[0].get_attribute('data-postblock'))
        profile_user = browser.find_element(By.ID, f"post-user-{post_id}")
        
        profile_user.click() #Click on Jane's post and ensure the profile view is displayed.
        wait.until(EC.presence_of_element_located((By.ID, "profile-view")))
        wait.until(EC.presence_of_element_located((By.ID, "follow-button")))
        
        profile_id = browser.find_element(By.ID, "profile-id").text
        self.assertEqual(profile_id, 'jane', "Check if the profile shown is for Jane")
        
        #Ensure Jane's 3 posting are shown
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertEqual(len(posting_blocks), 3, "Check there are 3 posting on this page by Jane")
        
        prev_post_ts = 0
        
        #For all the post on the profile-view, ensure all are Jane's and sorting order is correct.
        for posting in posting_blocks:
            post_id = int(posting.get_attribute('data-postblock'))
            post_user_id = browser.find_element(By.ID, f"post-user-{post_id}").text
            self.assertEqual(post_user_id, profile_id, "Check if the poster is Jane")
            post_ts = int(browser.find_element(By.ID, f"post-ts-u-{ post_id }").get_attribute("textContent"))
            if prev_post_ts == 0:
                prev_post_ts = post_ts
            self.assertGreaterEqual(prev_post_ts, post_ts, "Check timestamp order")

        #Ensure the Jane's followers and following counts are 0.
        followers_count = int(browser.find_element(By.ID, "followers-count").text)
        self.assertEqual(followers_count, 0, "Check if followers count is 0")
        
        followings_count = int(browser.find_element(By.ID, "followings-count").text)
        self.assertEqual(followings_count, 0, "Check if followings count is 0")
        
        #ensure the follow button is visible and the unfollow is not.
        follow_button = browser.find_element(By.ID, "follow-button")
        self.assertTrue(follow_button.is_displayed(), "check if the follow button is displayed.")
        self.assertTrue(follow_button.is_enabled(), "check if follow the button is enabled.")
        
        unfollow_button = browser.find_element(By.ID, "unfollow-button")
        self.assertFalse(unfollow_button.is_displayed(), "Check the unfollow is not displayed")
        
        follow_button.click() #Click follow
        wait.until(EC.text_to_be_present_in_element((By.ID, f"followers-count"), '1'))

        
        #Ensure followers count increases
        followers_count = int(browser.find_element(By.ID, "followers-count").text)
        self.assertEqual(followers_count, 1, "Check if followers count is 1")
        
        followings_count = int(browser.find_element(By.ID, "followings-count").text)
        self.assertEqual(followings_count, 0, "Check if followings count is 0")
        
        #Ensure the follow button is now not visible and the unfollow is visible.
        follow_button = browser.find_element(By.ID, "follow-button")
        self.assertFalse(follow_button.is_displayed(), "check the follow button is Not displayed.")
        
        unfollow_button = browser.find_element(By.ID, "unfollow-button")
        self.assertTrue(unfollow_button.is_displayed(), "Check the unfollow is displayed now")
        self.assertTrue(unfollow_button.is_enabled(), "check if the unfollow button is enabled.")

        unfollow_button.click() #Click unfollow
        wait.until(EC.text_to_be_present_in_element((By.ID, f"followers-count"), '0'))
        
        #Check follower count is back to 0 and only follow button is visible.
        followers_count = int(browser.find_element(By.ID, "followers-count").text)
        self.assertEqual(followers_count, 0, "Check if followers count is 0")
        
        followings_count = int(browser.find_element(By.ID, "followings-count").text)
        self.assertEqual(followings_count, 0, "Check if followings count is 0")
        
        follow_button = browser.find_element(By.ID, "follow-button")
        self.assertTrue(follow_button.is_displayed(), "check if the follow button is displayed.")
        self.assertTrue(follow_button.is_enabled(), "check if follow the button is enabled.")
        
        unfollow_button = browser.find_element(By.ID, "unfollow-button")
        self.assertFalse(unfollow_button.is_displayed(), "Check the unfollow is not displayed")
        
        follow_button.click() #Click follow again and leave on following on.
        wait.until(EC.text_to_be_present_in_element((By.ID, f"followers-count"), '1'))

        followers_count = int(browser.find_element(By.ID, "followers-count").text)
        self.assertEqual(followers_count, 1, "Check if followers count is 1")
                
        #Navigate back to all postings view.
        browser.find_element(By.ID, "allpost-nav").click()
        wait.until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertEqual(len(posting_blocks), 10, "Check there are 10 posting on this page")

        #Select Tim's post, the 4th post.
        post_id = int(posting_blocks[3].get_attribute('data-postblock'))
        profile_user = browser.find_element(By.ID, f"post-user-{post_id}")
        
        profile_user.click() #Click on Tim's post and check profile is displayed correctly
        wait.until(EC.presence_of_element_located((By.ID, "profile-view")))
        wait.until(EC.presence_of_element_located((By.ID, "follow-button")))
        
        profile_id = browser.find_element(By.ID, "profile-id").text
        self.assertEqual(profile_id, 'tim', "Check if the profile shown is for Tim")

        follow_button = browser.find_element(By.ID, "follow-button")
        self.assertTrue(follow_button.is_displayed(), "check if the follow button is displayed.")
 
        follow_button.click() #Follow Tim
        wait.until(EC.text_to_be_present_in_element((By.ID, f"followers-count"), '1'))
                
        #Navigate back to all posting view.
        browser.find_element(By.ID, "allpost-nav").click()
        wait.until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        #Navigate to page 3 of all posting view.
        wait.until(EC.element_to_be_clickable((By.ID, "select-page-button")))
        select_option = Select(browser.find_element(By.ID, "select-page"))
        select_button = browser.find_element(By.ID, "select-page-button")
        select_option.select_by_visible_text(str(3))
        select_button.submit() #Go to page 3
        
        wait.until(EC.presence_of_element_located((By.ID, "profile-view")))
        page_number = int(browser.find_element(By.ID, "page-number").text)
        self.assertEqual(page_number, 3, "Check if on the page")    
        
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertEqual(len(posting_blocks), 1, "Check there is 1 posting on this page")

        #Select the first post, tester's own post.
        post_id = int(posting_blocks[0].get_attribute('data-postblock'))
        profile_user = browser.find_element(By.ID, f"post-user-{post_id}")
        
        profile_user.click() #Click on sekar's post
        wait.until(EC.presence_of_element_located((By.ID, "profile-view")))
        
        #Ensure selar's profile is displayed.
        profile_id = browser.find_element(By.ID, "profile-id").text
        self.assertEqual(profile_id, 'sekar', "Check if the profile shown is for Sekar")

        #Check Following count.
        followings_count = int(browser.find_element(By.ID, "followings-count").text)
        self.assertEqual(followings_count, 2, "Check if followings count is 2")

        #ensure the follow and unfollow are not displayed.
        follow_buttons = browser.find_elements(By.ID, "follow-button")
        self.assertEqual(len(follow_buttons), 0, "Ensure no follow buttons")
        
        unfollow_buttons = browser.find_elements(By.ID, "unfollow-button")
        self.assertEqual(len(unfollow_buttons), 0, "Ensure no unfollow buttons")
                
        #logout and login as John.
        self.logout()
        self.login('john', self.tester_password)
        wait.until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        #Go to page 3.
        wait.until(EC.element_to_be_clickable((By.ID, "select-page-button")))
        select_option = Select(browser.find_element(By.ID, "select-page"))
        select_button = browser.find_element(By.ID, "select-page-button")
        select_option.select_by_visible_text(str(3))
        select_button.submit() #Go to page 3
        
        wait.until(EC.presence_of_element_located((By.ID, "profile-view")))
        page_number = int(browser.find_element(By.ID, "page-number").text)
        self.assertEqual(page_number, 3, "Check if on the page")    
        
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertEqual(len(posting_blocks), 1, "Check there is 1 posting on this page")

        post_id = int(posting_blocks[0].get_attribute('data-postblock'))
        profile_user = browser.find_element(By.ID, f"post-user-{post_id}")
        
        profile_user.click() #Click on sekar's post, and ensure on sekar's profile page
        wait.until(EC.presence_of_element_located((By.ID, "profile-view")))
        
        profile_id = browser.find_element(By.ID, "profile-id").text
        self.assertEqual(profile_id, 'sekar', "Check if the profile shown is for Sekar")

        #ensure followers and following counts are 0 and 2 and follow button is displayed.
        followers_count = int(browser.find_element(By.ID, "followers-count").text)
        self.assertEqual(followers_count, 0, "Check if followers count is 0")
        
        followings_count = int(browser.find_element(By.ID, "followings-count").text)
        self.assertEqual(followings_count, 2, "Check if followings count is 2")
        
        follow_button = browser.find_element(By.ID, "follow-button")
        self.assertTrue(follow_button.is_displayed(), "check if the follow button is displayed.")
        self.assertTrue(follow_button.is_enabled(), "check if follow the button is enabled.")
        
        unfollow_button = browser.find_element(By.ID, "unfollow-button")
        self.assertFalse(unfollow_button.is_displayed(), "Check the unfollow is not displayed")
        
        follow_button.click() #Click follow and check follower count is increased.
        wait.until(EC.text_to_be_present_in_element((By.ID, f"followers-count"), '1'))

        followers_count = int(browser.find_element(By.ID, "followers-count").text)
        self.assertEqual(followers_count, 1, "Check if followers count is 1")
        
        followings_count = int(browser.find_element(By.ID, "followings-count").text)
        self.assertEqual(followings_count, 2, "Check if followings count is 2")
        
           
    def tearDown(self):
        self.logout()
        self.browser.quit()
