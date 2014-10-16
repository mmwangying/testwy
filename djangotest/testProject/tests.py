from django.test import TestCase

# Create your tests here.
from django.test.client import Client
from django.utils import timezone
from polls.models import Poll

class PollTest(TestCase):
    def setUp(self):
        Poll.objects.create(question="lion", pub_date=timezone.now())
        Poll.objects.create(question="cat", pub_date=timezone.now())

    def test_lion_was_published_recently(self):
        """LION that can speak are correctly identified"""
        lion = Poll.objects.get(question="lion")
        self.assertEqual(lion.was_published_recently(), True)
    def test_cat_was_published_recently(self):
        """CAT that can speak are correctly identified"""        
        cat = Poll.objects.get(question="cat")
        self.assertEqual(cat.was_published_recently(), True)
    def test_httprequest(self):
        """Test Request"""
        c = Client()
        response = c.post('/admin/', {'username': 'admin', 'password': 'dd'})
        self.assertEqual(response.status_code, 200)
