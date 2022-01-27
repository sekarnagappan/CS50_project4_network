from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from password_generator import PasswordGenerator

from network.models import User, Postings, Followings, Likes
import json

class ProfileInquiryTestCase(TestCase):
    
    
    client = Client()
    tester = "sekar"
    pwo = PasswordGenerator()
    tester_password = pwo.generate()
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
        
    def test_view_profile(self):
        """
        Check Profiles page for a user.
        """
        test_profile_user = 'john'
        # Load index page
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        # Load profile view for john and assert positive response.
        response = self.client.get(reverse('view_profile') + '?profile_id=' + test_profile_user)
        self.assertEqual(response.status_code, 200)
        
        # Assert there are 12 posting records altogether.
        # Assert pagination returned page 1, and there are 2 pages altogether and sort order.
        
        self.assertEqual(response.context['count'], 12)
        self.assertEqual(response.context['postlist'].number, 1)
        self.assertEqual(response.context['postlist'].paginator.num_pages, 2)
        self.assertEqual(response.context['postlist'].paginator.per_page, 10)
        for i in range (0, len(response.context['postlist'])-1):
            self.assertTrue(response.context['postlist'][i].post_ts >= response.context['postlist'][i+1].post_ts)
            self.assertTrue(test_profile_user == response.context['postlist'][i].posting_user.username == response.context['postlist'][i+1].posting_user.username)

        self.assertEqual(response.context['profile_usr'], test_profile_user)
        self.assertEqual(response.context['followings'], 0)
        self.assertEqual(response.context['follows'], 0)
    
        
        # Request for page 2, and assert all response are as expected.
        response = self.client.get(reverse('view_profile') + '?profile_id=' + test_profile_user + '&page=2')
        self.assertEqual(response.context['postlist'].number, 2)
        self.assertEqual(response.context['postlist'].paginator.num_pages, 2)
        self.assertEqual(response.context['postlist'].paginator.per_page, 10)
        for i in range (0, len(response.context['postlist'])-1):
            self.assertTrue(response.context['postlist'][i].post_ts >= response.context['postlist'][i+1].post_ts)
            self.assertTrue(test_profile_user == response.context['postlist'][i].posting_user.username == response.context['postlist'][i+1].posting_user.username)
    
        # Request for a page greater then 2, and ensure the last page is returned.   
        response = self.client.get(reverse('view_profile') + '?profile_id='+ test_profile_user + '&page=444')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['postlist'].number, 2)
        self.assertEqual(len(response.context['postlist']), 2)

