from django.contrib.auth.models import User
from django.test import TestCase

from api.models import UserProfile, Animal


class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test', password='test')
        UserProfile.objects.create(balance=1000, user=user)

    def test_object_name_is_name(self):
        userprofile = UserProfile.objects.get(id=1)
        expected_object_name = userprofile.user.username
        self.assertEquals(expected_object_name, str(userprofile))
