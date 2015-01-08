from django.test import TestCase

# Create your tests here.
from app.models import Document as ls

class TestSufficiencies(TestCase):
    fixtures = ['lsds.yaml']

    def setUp(self):
        from django.conf import settings
        # call_setup_methods()
        pass
    
    def test_count_the_sufficiencies(self):
        # There are seven sufficiencies in the DB. Count them.
        print("There are 7 sufficiencies in the database")
        lsds = ls.objects.all()
        self.assertEqual(len(lsds), 7)

    def test_load_index(self):
        pass