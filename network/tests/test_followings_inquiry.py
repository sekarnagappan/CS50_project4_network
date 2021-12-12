from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from network.models import User, Postings, Followings, Likes
import json

class FollowingsInquiryTestCase(TestCase):
    """
    This test case setups up a user to follow 3 other users, and checks 
    the followings page displays all the post of the users followed.
    """
    client = Client()
    tester = "sekar"
    tester_password = "password"
    post_setup_count = 0
    post = []
    
    def setUp(self):

        """
        Create 5 users and set their passwords, and 21 post
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
                    [tim,   "Posting 4"],
                    [jane,  "Posting 5"],
                    [sekar, "Posting 6"],
                    [sekar, "Posting 7"],
                    [john,  "Posting 8"],
                    [john,  "Posting 9"],
                    [ann,   "Posting 10"],
                    [ann,   "Posting 11"],
                    [jane,  "Posting 12"],
                    [sekar, "Posting 13"],
                    [john,  "Posting 14"],
                    [ann,   "Posting 15"],
                    [tim,   "Posting 16"],
                    [jane,  "Posting 17"],
                    [sekar, "Posting 18"],
                    [sekar, "Posting 19"],
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
                
    def test_followings_count(self):
        """
        Test followings. For a user check if all the post for people one follows are retrieved.
        """
        self.assertEqual(User.objects.get(username=self.tester).followings_count, 0, "Check followings count")

        # Setup a user to follow 3 other users. 
               
        self.assertEqual(User.objects.get(username='john').followers_count, 0, "Check followers count")
        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': 'john', 'follow': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check followings registered successfully")
        self.assertEqual(User.objects.get(username='john').followers_count, 1, "Check followers count")
        
        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': 'ann', 'follow': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check followings registered successfully")
        
        response = self.client.post(reverse('follows'), 
                                    json.dumps({ 'profile_id': 'tim', 'follow': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check followings registered successfully")
        
        self.assertEqual(User.objects.get(username=self.tester).followings_count, 3, "Check followings count")
        
        #Retrieve the post of ones followings and check response.
        response = self.client.get(reverse('followings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 12, "Check followings post count")
        self.assertEqual(response.context['postlist'].number, 1, "Check if you are page 1")
        self.assertEqual(response.context['postlist'].paginator.num_pages, 2, "Check if there ate 2 pages")
        self.assertEqual(response.context['postlist'].paginator.per_page, 10, "Check if there are 10 per page")
        for i in range (0, len(response.context['postlist'])-1):
            self.assertTrue(response.context['postlist'][i].post_ts >= response.context['postlist'][i+1].post_ts, "Check sort order")
            self.assertIn(response.context['postlist'][i].posting_user.username, ['john', 'ann', 'tim'], "Check the post are for your followings")
        self.assertIn(response.context['postlist'][-1].posting_user.username, ['john', 'ann', 'tim'], "Check the post are for your followings")
        last_post_ts = response.context['postlist'][-1].post_ts

    
