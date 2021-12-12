from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from network.models import User, Postings, Followings, Likes
import json, logging

class FollowsTestCase(TestCase):
    """
    Testcase to test the follow and unfollow actions.
    """
    
    client = Client()
    tester = "sekar"
    tester_password = "password"
    post_setup_count = 0
    post = []
    
    def setUp(self):
        """
        Create 5 users and set their passwords, and 
        Create 21 postings for a few users and record their posting id
        Login to one user.
        """        
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
                                   last_name = "Timmy",
                                   email = "tim@mail.com",
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
                                    last_name = "Janes",
                                    email = "jane@mail.com",
                                    date_joined = timezone.now(),
                                    followers_count = 0,
                                    followings_count = 0
                                    )  
        jane.set_password(self.tester_password)
        jane.save()
        
        self.post = [   
                    [sekar, "Posting 1"],
                    [john,  "Posting 2"],
                    [ann,   "Posting 3"],
                    [john,   "Posting 4"],
                    [jane,  "Posting 5"],
                    [john, "Posting 6"],
                    [john, "Posting 7"],
                    [john,  "Posting 8"],
                    [john,  "Posting 9"],
                    [ann,   "Posting 10"],
                    [ann,   "Posting 11"],
                    [jane,  "Posting 12"],
                    [sekar, "Posting 13"],
                    [john,  "Posting 14"],
                    [john,   "Posting 15"],
                    [tim,   "Posting 16"],
                    [jane,  "Posting 17"],
                    [john, "Posting 18"],
                    [john, "Posting 19"],
                    [john,  "Posting 20"],
                    [john,  "Posting 21"]
         
                    ]
        
        self.post_setup_count = len(self.post)
        
        for p in self.post:
            posting = Postings.objects.create(
                                                posting_user=p[0],
                                                post_text=p[1],
                                                likes_count=0,
                                                dislikes_count=0,
                                                previous_post= None
                                            )
            p.append(posting.id)
            
        logged_in = self.client.login(username=self.tester, password=self.tester_password) 
        self.assertTrue(logged_in)    
        
        """Reduce the log level to avoid expected errors like 'not found'"""
        logger = logging.getLogger("django.request")
        logger.setLevel(logging.ERROR)
        
    def test_view_profile(self):
        """
        Check Profiles page for a user.
        """
        test_profile_user = 'john'
        
        self.assertEqual(User.objects.get(username=self.tester).followings_count, 0, "Check followings count")

        # Load profile view for john and assert positive response.
        self.assertEqual(User.objects.get(username=test_profile_user).followers_count, 0, "Check followers count")
        response = self.client.get(reverse('view_profile') + '?profile_id=' + test_profile_user)
        self.assertEqual(response.status_code, 200, "Check retrieval of profile page for one user")
        
        # Test to see if  logged in user can follow another.
        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': test_profile_user, 'follow': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Following updated!')
        self.assertEqual(content['followings_count'], 0)
        self.assertEqual(content['followers_count'], 1)
        self.assertEqual(content['user_follows'], 1)
        
        # Test to see if a user tries to follow a use who is already following.
        # This request should have been stopped at the front end, so this is back end check, just in case.
        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': test_profile_user, 'follow': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Following Anyway, nothing done!')
        self.assertEqual(User.objects.get(username=test_profile_user).followers_count, 1, "Check followers count")        
        self.assertEqual(User.objects.get(username=self.tester).followings_count, 1, "Check followings count")
                           

        #log in as another user and try to follow john. To check following counts are done correctly.
        logged_in = self.client.login(username='ann', password=self.tester_password) 
        self.assertTrue(logged_in) 
        
        response = self.client.get(reverse('view_profile') + '?profile_id=' + test_profile_user)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': test_profile_user, 'follow': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['followings_count'], 0)
        self.assertEqual(content['followers_count'], 2)
        self.assertEqual(content['user_follows'], 1)
        
        # Test unfollow.
        self.assertEqual(User.objects.get(username='ann').followings_count, 1, "Check followers count")
        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': test_profile_user, 'follow': False}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Following removed!')
        self.assertEqual(content['followings_count'], 0)
        self.assertEqual(content['followers_count'], 1)
        self.assertEqual(content['user_follows'], 0)
        self.assertEqual(User.objects.get(username='ann').followings_count, 0, "Check followers count")
        self.assertEqual(User.objects.get(username=test_profile_user).followers_count, 1, "Check followings count")

        
        # Test unfollow when not following.
        # This request should have been stopped at the front end, this is back end check, just in case.
        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': test_profile_user, 'follow': False}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Not Following Anyway, nothing done!')     
        
        # Test to check if a user can follow himself.
        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': 'ann', 'follow': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(content['error'], 'You cannot follow yourself.')     
        
        
        
        
            