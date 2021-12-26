from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from network.models import User, Postings, Followings, Likes
import json, logging

class InquiryPagingTestCase(TestCase):
    """
    Test All Posting Inquiry on the mail index page. 
    We are testing only yhe inquiry and paging here, not the posting.
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
        self.assertTrue(logged_in, "Check if login successful.")    
        
        """Reduce the log level warning to avoid expected errors like 'not found'"""
        logger = logging.getLogger("django.request")
        logger.setLevel(logging.ERROR)   
        
    def test_likes_dislikes(self):
        """
        Check registration of likes and dislikes.
        """

        # Like one post and dislike another, and check the like dislikes counts in the response and on the DB.
        # Also check ofr duplicate likes and dislikes.
        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[1][2], 'thumbs': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check Like registered ok")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Likes Registered.", "Check likes response message")
        self.assertEqual(content['likes_count'], 1, "Check likes count for post")
        self.assertEqual(content['dislikes_count'], 0, "Check dislikes count")
        
        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[1][2], 'thumbs': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 428, "Check duplicate registration is blocked")
        content = json.loads(response.content)
        self.assertEqual(content['error'], "You already liked this post!", "Check likes response message")
        

        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[2][2], 'thumbs': False}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check dislike registered ok")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Dislike Registered.", "Check likes response message")
        self.assertEqual(content['likes_count'], 0, "Check likes count for post")
        self.assertEqual(content['dislikes_count'], 1, "Check dislikes count")
        
        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[2][2], 'thumbs': False}),
                                    content_type="application/json"
                                    )
        
        self.assertEqual(response.status_code, 428, "Check duplicate registration is blocked")
        content = json.loads(response.content)
        self.assertEqual(content['error'], "You already disliked this post!", "Check likes response message")
    
        john_likes_count = Likes.objects.filter(liker=1, likes_active=True,post_id=self.post[1][2], likes=True).count()
        self.assertEqual(john_likes_count, 1)
        
        ann_dislikes_count = Likes.objects.filter(liker=1, likes_active=True, post_id=self.post[2][2], likes=False).count()
        self.assertEqual(ann_dislikes_count, 1)
                      
        #Login as Tim and like and dislike the same post. Count of likes and dislikes should increase to 2.
        logged_in = self.client.login(username='tim', password=self.tester_password) 
        self.assertTrue(logged_in, "Check if login successful.")    
        
        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[1][2], 'thumbs': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check Like registered ok")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Likes Registered.", "Check likes response message")
        self.assertEqual(content['likes_count'], 2, "Check likes count for post")
        self.assertEqual(content['dislikes_count'], 0, "Check dislikes count")
        

        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[2][2], 'thumbs': False}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check dislike registered ok")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Dislike Registered.", "Check likes response message")
        self.assertEqual(content['likes_count'], 0, "Check likes count for post")
        self.assertEqual(content['dislikes_count'], 2, "Check dislikes count")
        
        likes_count = Likes.objects.filter(likes_active=True,post_id=self.post[1][2], likes=True).count()
        self.assertEqual(likes_count, 2)
        
        dislikes_count = Likes.objects.filter(likes_active=True, post_id=self.post[2][2], likes=False).count()
        self.assertEqual(dislikes_count, 2)
          
        #Tim is flipping his likes and dislikes
        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[1][2], 'thumbs': False}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check Like registered ok")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Dislike Registered.", "Check likes response message")
        self.assertEqual(content['likes_count'], 1, "Check likes count for post")
        self.assertEqual(content['dislikes_count'], 1, "Check dislikes count")
        
        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[2][2], 'thumbs': True}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check dislike registered ok")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Likes Registered.", "Check likes response message")
        self.assertEqual(content['likes_count'], 1, "Check likes count for post")
        self.assertEqual(content['dislikes_count'], 1, "Check dislikes count")
        
        likes_count = Likes.objects.filter(likes_active=True,post_id=self.post[1][2], likes=True).count()
        self.assertEqual(likes_count, 1)
        dislikes_count = Likes.objects.filter(likes_active=True,post_id=self.post[1][2], likes=False).count()
        self.assertEqual(dislikes_count, 1)
        
        dislikes_count = Likes.objects.filter(likes_active=True, post_id=self.post[2][2], likes=False).count()
        self.assertEqual(dislikes_count, 1)
        likes_count = Likes.objects.filter(likes_active=True, post_id=self.post[2][2], likes=True).count()
        self.assertEqual(likes_count, 1)

        
        
        #Tim is removing his likes and dislikes
        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[1][2], 'thumbs': None}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check if likes cleared")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Likes Cleared.", "Check likes response message")
        self.assertEqual(content['likes_count'], 1, "Check likes count for post")
        self.assertEqual(content['dislikes_count'], 0, "Check dislikes count")
        
        response = self.client.post(reverse('thumbs_click'), 
                                    json.dumps({ 'post_id': self.post[2][2], 'thumbs': None}),
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201, "Check if dislikes cleared")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Likes Cleared.", "Check likes response message")
        self.assertEqual(content['likes_count'], 0, "Check likes count for post")
        self.assertEqual(content['dislikes_count'], 1, "Check dislikes count")
        
        likes_count = Likes.objects.filter(likes_active=True,post_id=self.post[1][2], likes=True).count()
        self.assertEqual(likes_count, 1)
        dislikes_count = Likes.objects.filter(likes_active=True,post_id=self.post[1][2], likes=False).count()
        self.assertEqual(dislikes_count, 0)
        
        dislikes_count = Likes.objects.filter(likes_active=True, post_id=self.post[2][2], likes=False).count()
        self.assertEqual(dislikes_count, 1)
        likes_count = Likes.objects.filter(likes_active=True, post_id=self.post[2][2], likes=True).count()
        self.assertEqual(likes_count, 0)