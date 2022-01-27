from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from django.utils import timezone
import logging
from password_generator import PasswordGenerator

from network.models import User, Postings, Followings, Likes

class BrowserNavigationTestCase(StaticLiveServerTestCase):
    """
    Test Paging, Check information on the page, counters, Sort Order.
    """
    test_browser = "Chrome"
    tester = "sekar"
    pwo = PasswordGenerator()
    tester_password = pwo.generate()
    post_setup_count = 0
    browser = ""
    test_browser = ""
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
                    
    def get_post_form_list(self, post_id):
        
        for p in self.post:
            if p[2] == post_id:
                return p
        
        #print(self.post)
        return ["","",0,0]

    def test_paging(self):
        """
        Test All Post inquiry, including paging, page count, posting counts, sort order.
        Setup 21 posting for 5 users and check the inquiry.
        """
        self.postings()
        
        self.logged_in_user = self.login(self.tester, self.tester_password)        

        browser = self.browser

        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        post_count = int(browser.find_element(By.ID, "post-count").text)
        self.assertEqual(post_count, len(self.post), "Check if there 21 post altogether")
        
        page_number = int(browser.find_element(By.ID, "page-number").text)
        self.assertEqual(page_number, 1, "Check if on page 1")
        
        total_pages = int(browser.find_element(By.ID, "total-pages").text)
        self.assertEqual(total_pages, 3, "Check if there are 3 pages")
        
        prev_post_ts = 0
        for page in range(1, total_pages+1):
            
            page_str = str(page)
            WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, "current-page"), page_str))

            page_number = int(browser.find_element(By.ID, "page-number").text)
            self.assertEqual(page_number, page, "Check if on the page")
            posting_blocks = browser.find_elements(By.NAME, "posting-block")
            if (page_number < total_pages):
                self.assertEqual(len(posting_blocks), 10, "Check there are 10 posting on this page")
            elif (page_number == total_pages):
                self.assertEqual(len(posting_blocks), (post_count % 10), "Check Remaining Posting on the last page")
            
            for posting in posting_blocks:
                post_id = int(posting.get_attribute('data-postblock'))
                post_user_id = browser.find_element(By.ID, f"post-user-{post_id}").text
                post_text = browser.find_element(By.ID, f"postings-body-{ post_id }").text
                post_ts = int(browser.find_element(By.ID, f"post-ts-u-{ post_id }").get_attribute("textContent"))
                if prev_post_ts == 0:
                    prev_post_ts = post_ts
                posted_item = self.get_post_form_list(post_id)
                self.assertEqual(post_user_id, posted_item[0], "Check the retrieved post is by the correct user")
                self.assertEqual(post_text, posted_item[1], "Check the posted text is as posted")
                self.assertGreaterEqual(prev_post_ts, post_ts, "Check timestamp order")
                
                #print(f"Post ID is {post_id} at {post_ts}")
            
            if page < total_pages:
                page_next = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "page-next")))
                browser.execute_script("arguments[0].click();", page_next)            
                #page_next.click()    
            else:
                page_next = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "no-page-next")))
                page_next = browser.find_element(By.ID, "no-page-next")
                
        for page in range(total_pages, 0, -1):
            
            page_number = int(browser.find_element(By.ID, "page-number").text)
            self.assertEqual(page_number, page, "Check if on page 3")
            posting_blocks = browser.find_elements(By.NAME, "posting-block")
            if (page_number < total_pages):
                self.assertEqual(len(posting_blocks), 10, "Check there are 10 posting on this page")
            elif (page_number == total_pages):
                self.assertEqual(len(posting_blocks), (post_count % 10), "Check Remaining Posting on the last page")
            
            if page > 1:
                page_prev = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "page-prev")))
                browser.execute_script("arguments[0].click();", page_prev)            
                #page_next.click()    
            else:
                page_prev = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "no-page-prev")))
                page_prev = browser.find_element(By.ID, "no-page-prev")


        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))

        for page in range(total_pages, 0, -1):

            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "select-page-button")))
            select_option = Select(browser.find_element(By.ID, "select-page"))
            select_button = browser.find_element(By.ID, "select-page-button")
            select_option.select_by_visible_text(str(page))
            select_button.submit()
            
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "select-page-button")))
            page_number = int(browser.find_element(By.ID, "page-number").text)
            self.assertEqual(page_number, page, "Check if on the page")        
        
    def tearDown(self):
        self.logout()
        self.browser.quit()
