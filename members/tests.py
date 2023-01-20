from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test.client import Client

from .models import UserProfile


class SignUpPageTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            age=69)

    def test_signup_page_status_code(self):
        response = self.client.get('/members/sign_up/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.user.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.user.email)
        self.assertEqual(get_user_model().objects.all()[0].age, self.user.age)


class UserProfileTests(TestCase):

    def setUp(self):

        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            age=420,
            password='Letmeout5!'
        )

        self.profile = UserProfile.objects.create(avatar='test_avatar.jpg', socials='hotmomsnearyou.com',
                                                  bio='netflix is overrated', user=self.user)

    def test_string_representation(self):
        profile = UserProfile(bio='HBO tv app sucks')
        self.assertEqual(str(profile.bio), profile.bio)

    def test_profile_content(self):
        self.assertEqual(self.profile.avatar, 'test_avatar.jpg')
        self.assertEqual(self.profile.socials, 'hotmomsnearyou.com')
        self.assertEqual(self.profile.bio, 'netflix is overrated')
        self.assertEqual(self.profile.user.username, 'testuser')

    def test_get_absolute_url(self):
        self.assertEqual(self.profile.get_absolute_url(), '/members/user_profile/1/')

    def test_user_profile_view(self):
        self.client.login(username='testuser', password='Letmeout5!')
        response = self.client.get(f'/members/user_profile/{self.profile.pk}/')
        print({self.profile.pk})
        no_response = self.client.get('/members/user_profile/11111/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'netflix is overrated')
        self.assertTemplateUsed(response, 'user_profile_details.html')
