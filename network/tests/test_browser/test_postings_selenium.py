from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from django.utils import timezone
from password_generator import PasswordGenerator

from network.models import User, Postings, Followings, Likes
import logging

class BrowserPostingTestCase(StaticLiveServerTestCase):
    """
    Test create and edit postings.
    """
    tester = "sekar"
    pwo = PasswordGenerator()
    tester_password = pwo.generate()
    post_setup_count = 0
    browser = ""
    test_browser = ""
    logged_in_user = ""
    post =  [
            ["sekar","Posting 1"],
            ["john", "Posting 2"],
            ["ann",  "Posting 3"],
            ["john", "Posting 4"],
            ["sekar","Posting 5"]
            ]

    
    def setUp(self):

        """
        Setup the webdriver
        Setup 5 Users
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
        """
        Login a user with the given id and password.
        Check you are on the index page
        """
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
        #print(f"User {logged_in_user}, logged in successfully.")

        return self.logged_in_user

    def logout(self):
        """
        Logout and check yu are in the login page.
        """

        browser = self.browser

        browser.find_element(By.ID, "logout-nav").click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "login-h2")))
        self.assertEqual(browser.find_element(By.ID, "login-h2").text, "Login", "Check you are on the login page")

    def test_postings(self):
        """
        Test creation of 5 postings and check the alert response.
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
                    #print(alert.text)
                    post_msg = alert.text
                    self.assertEqual(alert.text[0:31], "Response Message: Posting Done.", "Check the Response message on the alert")

                    alert.accept()
                    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

                    post_id = int(post_msg.split(':')[2])
                    p.append(post_id)

    def test_empty_postings(self):
        """
        Test an empty post. Ensure that it is not allowed.
        """

        browser = self.browser

        #logged_in_user = self.login(self.tester, self.tester_password)

        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        post_box = browser.find_element(By.ID, "postings-body")
        post_button = browser.find_element(By.ID, "posting-button")

        post_box.send_keys("")
        post_button.click()
        WebDriverWait(browser, 5, poll_frequency=0.5).until(EC.alert_is_present(), 'No Post made: Your posting text is empty!')

        alert = Alert(browser)
        #print(alert.text)
        self.assertEqual(alert.text, "No Post made: Your posting text is empty!", "Check the Response message on the alert")
        alert.accept()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

    def test_edit_post(self):
        """
        Test editing a post.
        Create a post, eidt it, and check if the edit is successful.
        """

        browser = self.browser

        #logged_in_user = self.login(self.tester, self.tester_password)

        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        post_box = browser.find_element(By.ID, "postings-body")
        post_button = browser.find_element(By.ID, "posting-button")

        post_box.send_keys("Post Data for Testing Edit")
        post_button.click()
        WebDriverWait(browser, 5, poll_frequency=0.5).until(EC.alert_is_present(), 'Response Message: Posting Done.')

        alert = Alert(browser)
        #print(alert.text)
        post_msg = alert.text
        self.assertEqual(alert.text[0:31], "Response Message: Posting Done.", "Check the Response message on the alert")

        alert.accept()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        post_id = int(post_msg.split(':')[2])

        edit_button = browser.find_element(By.ID, f"edit-{post_id}")
        edit_button.click()

        post_text = browser.find_element(By.ID, f"postings-body-{post_id}")
        new_text = post_text.text + "\nAdded a new line of text."

        post_text.clear()
        post_text.send_keys(new_text)

        post_button = browser.find_element(By.ID, f"post-{post_id}")
        post_button.click()

        WebDriverWait(browser, 5, poll_frequency=0.5).until(EC.alert_is_present(), 'Response Message: Posting Done.')

        alert = Alert(browser)
        #print(alert.text)
        post_msg = alert.text
        self.assertEqual(alert.text[0:31], "Response Message: Posting Done.", "Check the Response message on the alert")

        alert.accept()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        post_id = int(post_msg.split(':')[2])

        edited_text = browser.find_element(By.ID, f"postings-body-{post_id}").text
        self.assertEqual(edited_text, new_text, "Check the edited text has been saved")

    def test_edit_another_users_post(self):
        """
        Test edit a post created by a different user.
        Create a post with the default tester account and logout.
        Then log in as another user, and ensure the edit button is not available to edit the post.
        """
        browser = self.browser

        #logged_in_user = self.login(self.tester, self.tester_password)

        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        post_box = browser.find_element(By.ID, "postings-body")
        post_button = browser.find_element(By.ID, "posting-button")

        post_box.send_keys("Post Data for Testing Edit by another user")
        post_button.click()
        WebDriverWait(browser, 5, poll_frequency=0.5).until(EC.alert_is_present(), 'Response Message: Posting Done.')

        alert = Alert(browser)
        #print(alert.text)
        post_msg = alert.text
        self.assertEqual(alert.text[0:31], "Response Message: Posting Done.", "Check the Response message on the alert")

        alert.accept()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        post_id = int(post_msg.split(':')[2])

        self.logout()
        self.logged_in_user = self.login("john", self.tester_password)

        
        edit_button = browser.find_element(By.ID, f"edit-{post_id}")
        self.assertFalse(edit_button.is_displayed(), "Ensure the edit button is not displayed")
        with self.assertRaises(ElementNotInteractableException):
            edit_button.click() #clicking it should raise an exception.

        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))


    def tearDown(self):
        self.logout()
        self.browser.quit()
