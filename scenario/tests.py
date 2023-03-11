from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from .models import Movie, Genre, Director, Writer, Actor, Rating, MovieShelfRating, WatchedByUser
from members.models import UserProfile
from django.contrib.auth import get_user_model
from .forms import WatchedForm, ToWatchForm


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

    result_id_1 = 'tt1285016'
    result_id_2 = 'tt2975590'
    result_id_not_exists = 'tt1234567890'

    def setUp(self):
        self.genre = Genre.objects.create(genre_type='Comedy')
        self.director = Director.objects.create(name='Pixel The Director')
        self.writer = Writer.objects.create(name='Pixel The Writer')
        self.actor = Actor.objects.create(name='Just Pixel')
        self.rating = Rating.objects.create(source='Internet Movie Database', value='9.8/10')

        self.movie = Movie.objects.create(
            Title='Pixels Life',
            Year='2023',
            Rated='18',
            Released='10 Feb 2023',
            Runtime='169',
            Plot='Life of best dog ever.',
            Language='English',
            Country='Poland',
            Awards='Oscar',
            Poster='posters/test_movie.jpg',
            Poster_url='https://www.test.com/test_movie.jpg',
            Metascore='75',
            imdbRating='7.6',
            imdbVotes='12,345',
            imdbID='tt1234567',
            Type='movie',
            DVD='N/A',
            BoxOffice='21370000 $',
            Production='Pixel Studio',
            Website='https://www.pixelslife.com',
            totalSeasons='',
        )
        self.movie.Genre.set([self.genre])
        self.movie.Director.set([self.director])
        self.movie.Writer.set([self.writer])
        self.movie.Actors.set([self.actor])
        self.movie.Rating.set([self.rating])

    def test_movie_detail_view_result_correctly_stored_in_db(self):
        response = self.client.get(reverse('movie_details', args=[self.movie.imdbID]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.Title)
        self.assertContains(response, self.movie.Year)
        self.assertContains(response, self.movie.Rated)
        self.assertContains(response, self.movie.Released)
        self.assertContains(response, self.movie.Runtime)
        self.assertContains(response, self.movie.Plot)
        self.assertContains(response, self.movie.Language)
        self.assertContains(response, self.movie.Country)
        self.assertContains(response, self.movie.Awards)
        self.assertContains(response, self.movie.Poster)
        self.assertContains(response, self.movie.Metascore)
        self.assertContains(response, self.movie.imdbRating)
        self.assertContains(response, self.movie.imdbVotes)
        self.assertContains(response, self.movie.Type)
        self.assertContains(response, self.movie.DVD)
        self.assertContains(response, self.movie.BoxOffice)
        self.assertContains(response, self.movie.Production)
        self.assertContains(response, self.movie.Website)
        self.assertContains(response, self.movie.totalSeasons)

    def test_movie_detail_view_status_code_valid_id(self):
        response = self.client.get(reverse('movie_details', args=[self.result_id_1]))
        self.assertEqual(response.status_code, 200)

    def test_movie_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('movie_details', args=[self.result_id_2]))
        self.assertTemplateUsed(response, 'movie_details.html')

    # Add exceptions (key error not 404)
    # def test_movie_detail_view_status_code_invalid_id(self):
    #     response = self.client.get(reverse('movie_details', args=[self.result_id_not_exists]))
    #     self.assertEqual(response.status_code, 404)


class MovieDetailsViewFormsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.movie1 = Movie.objects.create(Title='Test Movie',
                                          Year='2023',
                                          Rated='18',
                                          Released='10 Feb 2023',
                                          Runtime='169',
                                          Plot='Life of best dog ever.',
                                          Language='English',
                                          Country='Poland',
                                          Awards='Oscar',
                                          Poster='posters/test_movie.jpg',
                                          Poster_url='https://www.test.com/test_movie.jpg',
                                          Metascore='75',
                                          imdbRating='7.6',
                                          imdbVotes='12,345',
                                          imdbID='tt1234567',
                                          Type='movie',
                                          DVD='N/A',
                                          BoxOffice='21370000 $',
                                          Production='Pixel Studio',
                                          Website='https://www.pixelslife.com',
                                          totalSeasons='',
                                          )

        self.movie2 = Movie.objects.create(Title='Test Movie2',
                                           Year='2023',
                                           Rated='18',
                                           Released='10 Feb 2023',
                                           Runtime='169',
                                           Plot='Life of best dog ever.',
                                           Language='English',
                                           Country='Poland',
                                           Awards='Oscar',
                                           Poster='posters/test_movie.jpg',
                                           Poster_url='https://www.test.com/test_movie.jpg',
                                           Metascore='75',
                                           imdbRating='7.6',
                                           imdbVotes='12,345',
                                           imdbID='tt1234576',
                                           Type='movie',
                                           DVD='N/A',
                                           BoxOffice='21370069 $',
                                           Production='Pixel Studio 2',
                                           Website='https://www.pixelslife.com',
                                           totalSeasons='',
                                           )

    def test_form_add_to_watched_valid_data(self):
        form = WatchedForm(data=self.movie1.pk)
        self.assertTrue(form.is_valid())

    def test_form_add_to_watched_no_data(self):
        form = WatchedForm(data=None)
        self.assertFalse(form.is_valid())

    def test_watched_form_in_movie_details_view(self):
        response = self.client.post('/scenario/result/tt0372784', {'watched': 'valid_movie_data'})
        self.assertEqual(response.status_code, 200)

    def test_form_add_to_to_watch_valid_data(self):
        form = ToWatchForm(data=self.movie2.pk)
        self.assertTrue(form.is_valid())

    def test_form_add_to_to_watch_no_data(self):
        form = ToWatchForm(data=None)
        self.assertFalse(form.is_valid())

    def test_to_watch_form_in_movie_details_view(self):
        response = self.client.post('/scenario/result/tt0372784', {'to_watch': 'valid_movie_data'})
        self.assertEqual(response.status_code, 200)

    def test_forms_in_movie_details_view_contain_csrf(self):
        response = self.client.get('/scenario/result/tt0372784')
        self.assertContains(response, 'csrfmiddlewaretoken')


class ActorDetailsViewTests(TestCase):

    def setUp(self):
        self.actor = Actor.objects.create(name="Rzerard Pike")

    def test_actor_details_view_returns_200_for_existing_actor(self):
        response = self.client.get(f'/scenario/actor/{self.actor.slug}')
        self.assertEqual(response.status_code, 200)

    def test_actor_details_view_returns_200_for_existing_actor_by_url_name(self):
        response = self.client.get(reverse('actor_detail', args=[self.actor.slug]))
        self.assertEqual(response.status_code, 200)

    def test_actor_details_view_returns_404_for_non_existing_actor(self):
        response = self.client.get('/scenario/actor/SelenaGomez')
        self.assertEqual(response.status_code, 404)

    def test_actor_details_view_uses_correct_template(self):
        response = self.client.get(f'/scenario/actor/{self.actor.slug}')
        self.assertTemplateUsed(response, 'actor_details.html')

    def test_actor_details_view_displays_actor_details(self):
        response = self.client.get(f'/scenario/actor/{self.actor.slug}')
        self.assertContains(response, self.actor.name)


class DirectorDetailsViewTests(TestCase):

    def setUp(self):
        self.director = Director.objects.create(name="Vince Gilligan ")

    def test_director_details_view_returns_200_for_existing_actor(self):
        response = self.client.get(f'/scenario/director/{self.director.slug}')
        self.assertEqual(response.status_code, 200)

    def test_director_details_view_returns_200_for_existing_actor_by_url_name(self):
        response = self.client.get(reverse('director_detail', args=[self.director.slug]))
        self.assertEqual(response.status_code, 200)

    def test_director_details_view_returns_404_for_non_existing_actor(self):
        response = self.client.get('/scenario/director/QuentinoTarantoto')
        self.assertEqual(response.status_code, 404)

    def test_director_details_view_uses_correct_template(self):
        response = self.client.get(f'/scenario/director/{self.director.slug}')
        self.assertTemplateUsed(response, 'director_details.html')

    def test_director_details_view_displays_director_details(self):
        response = self.client.get(f'/scenario/director/{self.director.slug}')
        self.assertContains(response, self.director.name)


class WriterDetailsViewTests(TestCase):

    def setUp(self):
        self.writer = Writer.objects.create(name='Yann Martel')

    def test_writer_details_view_returns_200_for_existing_actor(self):
        response = self.client.get(f'/scenario/writer/{self.writer.slug}')
        self.assertEqual(response.status_code, 200)

    def test_writer_details_view_returns_200_for_existing_actor_by_url_name(self):
        response = self.client.get(reverse('writer_detail', args=[self.writer.slug]))
        self.assertEqual(response.status_code, 200)

    def test_writer_details_view_returns_404_for_non_existing_writer(self):
        response = self.client.get('/scenario/writer/KrystynaNolan')
        self.assertEqual(response.status_code, 404)

    def test_writer_details_view_uses_correct_template(self):
        response = self.client.get(f'/scenario/writer/{self.writer.slug}')
        self.assertTemplateUsed(response, 'writer_details.html')

    def test_writer_details_view_displays_writer_details(self):
        response = self.client.get(f'/scenario/writer/{self.writer.slug}')
        self.assertContains(response, self.writer.name)


class GenreDetailsViewTests(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(genre_type='Thriller')

    def test_genre_details_view_returns_200_for_existing_genre(self):
        response = self.client.get(f'/scenario/genre/{self.genre.slug}')
        self.assertEqual(response.status_code, 200)

    def test_genre_details_view_returns_200_for_existing_genre_by_url_name(self):
        response = self.client.get(reverse('genre_type', args=[self.genre.slug]))
        self.assertEqual(response.status_code, 200)

    def test_genre_details_view_returns_404_for_non_existing_genre(self):
        response = self.client.get('/scenario/genre/YourJokes')
        self.assertEqual(response.status_code, 404)

    def test_genre_details_view_uses_correct_template(self):
        response = self.client.get(f'/scenario/genre/{self.genre.slug}')
        self.assertTemplateUsed(response, 'genre_details.html')

    def test_genre_details_view_displays_genre_details(self):
        response = self.client.get(f'/scenario/genre/{self.genre.slug}')
        self.assertContains(response, self.genre.genre_type)
