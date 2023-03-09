from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/scenario/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_status_code_if_query(self):
        response = self.client.get('/scenario/?q=test')
        self.assertEqual(response.status_code, 200)

    def test_home_page_status_code_if_query_with_two_words(self):
        response = self.client.get('/scenario/?q=test+test')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_if_query(self):
        response = self.client.get('/scenario/?q=test')
        self.assertTemplateUsed(response, 'search_results.html')

    def test_view_uses_correct_template_if_with_two_words(self):
        response = self.client.get('/scenario/?q=test+test')
        self.assertTemplateUsed(response, 'search_results.html')

    def test_home_page_status_code_if_query_without_q_param(self):
        no_response = self.client.get('/scenario/=test')
        self.assertEqual(no_response.status_code, 404)

    def test_home_page_status_code_if_empty_query(self):
        response = self.client.get('/scenario/?q=')
        self.assertEqual(response.status_code, 200)

    def test_home_page_templated_used_if_empty_query(self):
        response = self.client.get('/scenario/?q=')
        self.assertTemplateUsed(response, 'home.html')

    # Add exceptions (key error not 404)
    # def test_home_page_status_code_if_no_results(self):
    #     no_response = self.client.get('/scenario/?q=dsadasdasdad')
    #     self.assertEqual(no_response.status_code, 404)
    #
    # # Add exceptions (key error not 404)
    # def test_home_page_status_code_if_page_not_exists(self):
    #     no_response = self.client.get('/scenario/?q=test&page=42000')
    #     self.assertEqual(no_response.status_code, 404)


class MovieDetailsViewTests(TestCase):

    def test_movie_detail_view_status_code_valid_id(self):
        response = self.client.get()