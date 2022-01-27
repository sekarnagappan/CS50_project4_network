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
import logging, time
from password_generator import PasswordGenerator

from network.models import User, Postings, Followings, Likes

class BrowserLikesTestCase(StaticLiveServerTestCase):
    """
    Test case to test likes and dislikes
    """
    test_browser = ""
    tester = "sekar"
    logged_in_user = ""
    pwo = PasswordGenerator()
    tester_password = pwo.generate()
    post_setup_count = 0
    browser = ""
    post = [
            ["sekar","Posting 1"],
            ["tim", "Posting 2"],
            ["ann",  "Posting 3"],
            ["tim",  "Posting 4"],
            ["jane", "Posting 5"],
            ["jane", "Posting 6"]
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
        browser.get(f"{self.live_server_url}/login")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "login_button")))

        # browser.execute_script("window.scrollTo(0,0)")
        # logout_nav_loc = browser.find_element(By.ID, "logout-nav").location_once_scrolled_into_view
        # logout_nav = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "logout-nav")) )
        # logout_nav.click()
        # WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "login-h2")))
        # self.assertEqual(browser.find_element(By.ID, "login-h2").text, "Login", "Check you are on the login page")

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
                    
    def thumbs_click(self, browser, up_down_ind, postings_block, increment):
        
        post_id = int(postings_block.get_attribute('data-postblock'))
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        thumbs = browser.find_element(By.ID, f"thumbs-{up_down_ind}-{post_id}")
        if up_down_ind == "up":
            count = int(browser.find_element(By.ID, f"likes-count-{post_id}").text)
        else:
            count = int(browser.find_element(By.ID, f"unlikes-count-{post_id}").text)

        
        likes_switch = thumbs.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "off", "Check likes is off for the first post")
        self.assertEqual(thumbs.value_of_css_property('color'),'rgba(0, 0, 0, 1)', "Check if color is black")

        thumbs.click() #Click thumbs up.
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"likes-count-{post_id}"), str(count+increment)))
        
      
        likes_switch = thumbs.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "on", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"likes-count-{post_id}").text), count + increment, "Check likes count increases by 1")
        self.assertEqual(thumbs.value_of_css_property('color'),'rgba(255, 0, 0, 1)', "Check if color is red")       
                    
    def test_likes(self):
        """
        Test Likes and dislikes.
        """
        
        self.postings()
                
        browser = self.browser

        self.logged_in_user = self.login(self.tester, self.tester_password)

        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))
        
        post_count = int(browser.find_element(By.ID, "post-count").text)
        self.assertGreaterEqual(post_count, 5, "Check if there are more then 5 post")
        
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertGreaterEqual(len(posting_blocks), 5, "Check there are more then 5 posting on this page")
        
        # Test for likes and removal of likes. For the first post, 
        # 1. ensure likes is zero and the thumbs up button is black
        # 2. click thumbs up
        # 3. Check likes count increased by and color is red.
        # 4. Click thumbs up again
        # 5. Ensure the likes in decreased by 1, and the color reverts to black.
        
        post_id = int(posting_blocks[0].get_attribute('data-postblock'))
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        thumbs_up = browser.find_element(By.ID, f"thumbs-up-{post_id}")
        likes_count = int(browser.find_element(By.ID, f"likes-count-{post_id}").text)
        
        likes_switch = thumbs_up.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "off", "Check likes is off for the first post")
        self.assertEqual(thumbs_up.value_of_css_property('color'),'rgba(0, 0, 0, 1)', "Check if color is black")

        thumbs_up.click() #Click thumbs up.
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"likes-count-{post_id}"), str(likes_count+1)))
        
      
        likes_switch = thumbs_up.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "on", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"likes-count-{post_id}").text), likes_count + 1, "Check likes count increases by 1")
        self.assertEqual(thumbs_up.value_of_css_property('color'),'rgba(255, 0, 0, 1)', "Check if color is red")
        
        thumbs_up.click() # Click thumbs up again and the like should be removed.
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"likes-count-{post_id}"), str(likes_count)))
       
        likes_switch = thumbs_up.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "off", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"likes-count-{post_id}").text), likes_count, "Check likes count decreases by 1")
        self.assertEqual(thumbs_up.value_of_css_property('color'),'rgba(0, 0, 0, 1)', "Check if color is black")
 
        # Similar to the like test, Test for dislikes and removal of dislikes
        post_id = int(posting_blocks[1].get_attribute('data-postblock'))
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        thumbs_down = browser.find_element(By.ID, f"thumbs-down-{post_id}")
        dislikes_count = int(browser.find_element(By.ID, f"dislikes-count-{post_id}").text)
  
        likes_switch = thumbs_down.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "off", "Check likes are off")
        self.assertEqual(thumbs_down.value_of_css_property('color'),'rgba(0, 0, 0, 1)', "Check if color is black")

        thumbs_down.click() #Dislike
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"dislikes-count-{post_id}"), str(dislikes_count+1)))
        
        likes_switch = thumbs_down.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "on", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"dislikes-count-{post_id}").text), dislikes_count + 1, "Check likes count increases by 1")
        self.assertEqual(thumbs_down.value_of_css_property('color'),'rgba(255, 0, 0, 1)', "Check if color is red")
        
        thumbs_down.click() #Remove Dislike
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"dislikes-count-{post_id}"), str(dislikes_count)))
        
        likes_switch = thumbs_down.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "off", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"dislikes-count-{post_id}").text), dislikes_count, "Check likes count decreases by 1") 
        self.assertEqual(thumbs_down.value_of_css_property('color'),'rgba(0, 0, 0, 1)', "Check if color is black")
        
        #Test a like, and then flip to dislike.
        post_id = int(posting_blocks[2].get_attribute('data-postblock'))
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        thumbs_up = browser.find_element(By.ID, f"thumbs-up-{post_id}")
        likes_count = int(browser.find_element(By.ID, f"likes-count-{post_id}").text)
        
        likes_switch = thumbs_up.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "off", "Check likes are off for me")
        self.assertEqual(thumbs_up.value_of_css_property('color'),'rgba(0, 0, 0, 1)', "Check if color is black")

        thumbs_up.click() #Like
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"likes-count-{post_id}"), str(likes_count+1)))
        
        likes_switch = thumbs_up.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "on", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"likes-count-{post_id}").text), likes_count + 1, "Check likes count increases by 1")
        self.assertEqual(thumbs_up.value_of_css_property('color'),'rgba(255, 0, 0, 1)', "Check if color is red")
        
        #flip the like to dislike
        thumbs_down = browser.find_element(By.ID, f"thumbs-down-{post_id}")
        dislikes_count = int(browser.find_element(By.ID, f"dislikes-count-{post_id}").text)
        
        likes_switch = thumbs_down.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "off", "Check likes are off for me")
        self.assertEqual(thumbs_down.value_of_css_property('color'),'rgba(0, 0, 0, 1)', "Check if color is black")

        thumbs_down.click() # Click thumbs down, should switch a like to a dislike
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"dislikes-count-{post_id}"), str(dislikes_count+1)))
        
        likes_switch = thumbs_down.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "on", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"dislikes-count-{post_id}").text), dislikes_count + 1, "Check likes count increases by 1")
        self.assertEqual(thumbs_down.value_of_css_property('color'),'rgba(255, 0, 0, 1)', "Check if color is red")
              
        likes_switch = thumbs_up.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "off", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"likes-count-{post_id}").text), likes_count, "Check likes count decreases by 1")
        self.assertEqual(thumbs_up.value_of_css_property('color'),'rgba(0, 0, 0, 1)', "Check if color is black")
        
        
        #Test like and dislike a post from 2 different 2 users
        post_id = int(posting_blocks[0].get_attribute('data-postblock'))
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        thumbs_up = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.ID, f"thumbs-up-{post_id}")))
        likes_count = int(browser.find_element(By.ID, f"likes-count-{post_id}").text)

        thumbs_up.click()
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"likes-count-{post_id}"), str(likes_count+1)))

        post_id = int(posting_blocks[1].get_attribute('data-postblock'))
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        thumbs_down = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.ID, f"thumbs-down-{post_id}")))
        dislikes_count = int(browser.find_element(By.ID, f"dislikes-count-{post_id}").text)

        thumbs_down.click()
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"dislikes-count-{post_id}"), str(dislikes_count+1)))

        self.logout()
        self.logged_in_user = self.login('john', self.tester_password)
 
        # Login as John and like and dislike the same 2 post as above, and ensure count increases to 2.
        browser.get(f"{self.live_server_url}/index")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "newpost-h5")))  
        
        posting_blocks = browser.find_elements(By.NAME, "posting-block")
        self.assertGreaterEqual(len(posting_blocks), 5, "Check there are more then 4 posting on this page")  
             
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #Like and dislike the same two post
        post_id = int(posting_blocks[0].get_attribute('data-postblock'))
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        thumbs_up = browser.find_element(By.ID, f"thumbs-up-{post_id}")
        likes_count = int(browser.find_element(By.ID, f"likes-count-{post_id}").text)
 
        thumbs_up.click()
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"likes-count-{post_id}"), str(likes_count+1)))
        
        likes_switch = thumbs_up.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "on", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"likes-count-{post_id}").text), likes_count + 1, "Check likes count increases by 1")
        self.assertEqual(thumbs_up.value_of_css_property('color'),'rgba(255, 0, 0, 1)', "Check if color is red")
        
        # Dislike the same post 
        post_id = int(posting_blocks[1].get_attribute('data-postblock'))
        post_block = browser.find_element(By.ID, f"posting-block-{post_id}").location_once_scrolled_into_view
        thumbs_down = browser.find_element(By.ID, f"thumbs-down-{post_id}")
        dislikes_count = int(browser.find_element(By.ID, f"dislikes-count-{post_id}").text)

        thumbs_down.click()    
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.ID, f"dislikes-count-{post_id}"), str(dislikes_count+1)))
        
        likes_switch = thumbs_down.get_attribute('data-likes') 
        self.assertEqual(likes_switch, "on", "Check likes is on for me")
        self.assertEqual(int(browser.find_element(By.ID, f"dislikes-count-{post_id}").text), dislikes_count + 1, "Check likes count increases by 1")
        self.assertEqual(thumbs_down.value_of_css_property('color'),'rgba(255, 0, 0, 1)', "Check if color is red")        
        
    def tearDown(self):
        self.browser.quit()
