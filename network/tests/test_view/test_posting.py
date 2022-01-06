from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from network.models import User, Postings, Followings, Likes
import json, logging

class NetworkTestCase(TestCase):
    """
    Test create and edit postings.
    """
    
    client = Client()
    tester = "sekar"
    tester_password = "password"
    post_setup_count = 0
    post = []
    
    def setUp(self):

        """
        Create 3 users and set their passwords, and 
        Create 4 postings for a few users and record their posting id.
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


        
        self.post = [   
                    [sekar, "Posting 1"],
                    [john,  "Posting 2"],
                    [ann,   "Posting 2"],
                    [sekar, "Posting 3"]
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
        
        """Reduce the log level warning to avoid expected errors like 'not found'"""
        logger = logging.getLogger("django.request")
        logger.setLevel(logging.ERROR)
        
    def test_create_post(self):
        """
        Test create a new post
        """

        # Get a pre count of all posting records
        # Make a posting and assert response status and message is as expected.
        pre_count = Postings.objects.count()      
        post_text = "Post Text No. 1"  
        response = self.client.post(reverse('make_posting'), 
                                    json.dumps({'text': post_text, 'post_id': None}), 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201, "Check correct response")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Posting Done.", "Check response message")
        
        # Get a count of all posting records from DB
        # Assert one record added.
        post_count = Postings.objects.count()
        self.assertEqual(post_count, pre_count + 1, "Check number of posting records increased by 1")
        
        # Get record using key from response message and assert posting text is as expected.
        posting_pk = content['posting_pk']
        posting = Postings.objects.get(pk=posting_pk)
        #print(f"inserted Posting: {posting.id}, text: {posting.post_text} by: {posting.posting_user}")
        self.assertEqual(posting.post_text, post_text, "check postings text on the database")
        
    def test_create_empty_post(self):
        """
        Test create an empty post and assert posting is rejected.
        """
        
        pre_count = Postings.objects.count()      
        post_text = ""  
        response = self.client.post(reverse('make_posting'), 
                                    json.dumps({'text': post_text, 'post_id': None}), 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 405, "Check expected negative response")
        content = json.loads(response.content)
        self.assertEqual(content['error'], "Your post is empty.", "Check response error as expected")
        
        post_count = Postings.objects.count()
        self.assertEqual(post_count, pre_count, "Check postings count did not change")
    
    def test_edit_post(self):
        """
        Test Edit your own Post and assert the post is successful and all DB records as expected.
        """
        
        # Take a count of all posting records.
        # Get the 4 posting record. Should belong to the current user.
        # Change the text and post it.
        # Assert if correct response received.
        edit_key = self.post[3][2]
        pre_count = Postings.objects.count()
        posting = Postings.objects.get(pk=edit_key)      
        post_text = posting.post_text + " - " + "Edit Post 1"  
        response = self.client.post(reverse('make_posting'), 
                                    json.dumps({'text': post_text, 'post_id': posting.id}), 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201, "Check correct response")
        content = json.loads(response.content)
        self.assertEqual(content['message'], "Posting Done.", "Check Response Message")
        
        # Get a posting count of all records and assert if one record added.
        post_count = Postings.objects.count()
        self.assertEqual(post_count, pre_count + 1, "Check total number of posting records increased by 1")

        # Get a posting count of all active records (not superceded) and assert equals previous.
        post_count = Postings.objects.filter(post_superceded=False).count()
        self.assertEqual(post_count, pre_count, "Check total number of active posting records is the same")
        
        # Get the the newly edited record using the key return by the post response
        # Assert the content is the edit content and the records point to the previous version of the record.
        posting_pk = content['posting_pk']
        new_posting = Postings.objects.get(pk=posting_pk)
        #print(f"inserted Posting: {posting.id}, text: {posting.post_text} by: {posting.posting_user}")
        self.assertEqual(new_posting.post_text, post_text, "Check posting text is the amended text")
        self.assertEqual(new_posting.previous_post.id, edit_key, "Check Edit Record new key")
        
        # Get record from database and asset record superceded.
        posting = Postings.objects.get(pk=edit_key) 
        self.assertTrue(posting.post_superceded, "Check original record has been superceeded")
        
        #Refresh the index page and ensure the first record is the edited record.
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['postlist'][0].id, new_posting.id, "Check the edit record is the first on index page")

        
        
    def test_edit_others_post(self):
        """
        Test Edit some else's Post and ensure the request is rejected.
        """
        edit_key = self.post[1][2]
        pre_count = Postings.objects.count()
        posting = Postings.objects.get(pk=edit_key)      
        post_text = posting.post_text + " - " + "Edit Post 1"  
        response = self.client.post(reverse('make_posting'), 
                                    json.dumps({'text': post_text, 'post_id': posting.id}), 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 403, "Check expected response code")
        content = json.loads(response.content)
        self.assertEqual(content['error'], "You cannot edit this post.", "Check error message")
        
        post_count = Postings.objects.count()
        self.assertEqual(post_count, pre_count, "Check record count did not change.")
   
    
