from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from network.models import User, Postings, Followings, Likes
import json

class LoginTestCase(TestCase):
    
    client = Client()
    tester = "tester"
    tester_password = "password"
    post_setup_count = 0
    post = []
    
    def setUp(self):

        """
        Create 5 users and set their passwords
        """        
        test_user = User.objects.create( username = self.tester, 
                                         is_superuser = False,
                                         is_staff = False,
                                         is_active = True,
                                         first_name = "Tester",
                                         last_name = "Tester",
                                         email = "tester@mail.com",
                                         date_joined = timezone.now(),
                                         followers_count = 0,
                                         followings_count = 0
                                         )
        test_user.set_password(self.tester_password)
        test_user.save()

        test_user2 = User.objects.create( username = self.tester + "2", 
                                          is_superuser = False,
                                          is_staff = False,
                                          is_active = True,
                                          first_name = "Tester2",
                                          last_name = "Tester",
                                          email = "tester2@mail.com",
                                          date_joined = timezone.now(),
                                          followers_count = 0,
                                          followings_count = 0
                                        )
        test_user2.set_password(self.tester_password)
        test_user2.save()

                    
    def test_user_counts(self):
        """
        Test 2 user have been setup.
        """
        count = User.objects.count()
        self.assertEqual(User.objects.all().count(), 2, "Count no of user is 2")
        
    def test_valid_login(self):
        """
        Test Valid  login
        """
        
        logged_in = self.client.login(username=self.tester, password=self.tester_password) 
        self.assertTrue(logged_in)

        response = self.client.post('/login', {'username': self.tester, 'password': self.tester_password})
        self.assertEqual(response.status_code, 302)
    
    def test_invalid_login(self):
        """
        Test Invalid login
        """
        
        logged_in = self.client.login(username=self.tester, password="12345678") 
        self.assertFalse(logged_in)
        
        response = self.client.post('/login', {'username': self.tester, 'password': '12345678'})
        self.assertEqual(response.status_code, 200)
        
