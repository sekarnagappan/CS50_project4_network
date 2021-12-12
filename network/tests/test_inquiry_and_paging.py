from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from network.models import User, Postings, Followings, Likes
import json

class InquiryPagingTestCase(TestCase):
    
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
        
    def test_get_index_and_paging_count(self):
        """
        Check if a given number of post exist in the response and the paginations counts.
        """

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], self.post_setup_count)
        self.assertEqual(response.context['postlist'].number, 1)
        self.assertEqual(response.context['postlist'].paginator.num_pages, 3)
        self.assertEqual(response.context['postlist'].paginator.per_page, 10)
        for i in range (0, len(response.context['postlist'])-1):
            self.assertTrue(response.context['postlist'][i].post_ts >= response.context['postlist'][i+1].post_ts)
        last_post_ts = response.context['postlist'][0].post_ts
        
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], self.post_setup_count)
        self.assertEqual(response.context['postlist'].number, 2)
        self.assertEqual(response.context['postlist'].paginator.num_pages, 3)
        self.assertEqual(response.context['postlist'].paginator.per_page, 10)
        self.assertTrue(last_post_ts >= response.context['postlist'][0].post_ts)
        for i in range (0, len(response.context['postlist'])-1):
            self.assertTrue(response.context['postlist'][i].post_ts >= response.context['postlist'][i+1].post_ts)
        
        response = self.client.get(reverse('index') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['postlist'].number, 3)
        self.assertEqual(len(response.context['postlist']), 1)
        self.assertTrue(last_post_ts >= response.context['postlist'][0].post_ts)
        for i in range (0, len(response.context['postlist'])-1):
            self.assertTrue(response.context['postlist'][i].post_ts >= response.context['postlist'][i+1].post_ts)

        response = self.client.get(reverse('index') + '?page=4444')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['postlist'].number, 3)
        self.assertEqual(len(response.context['postlist']), 1)



    
