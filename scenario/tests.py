from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse
from .models import Movie, Genre, Director, Writer, Actor, Rating, MovieShelfRating, WatchedByUser, ToWatchByUser
from members.models import UserProfile
from django.contrib.auth import get_user_model
from .forms import WatchedForm, ToWatchForm
from django.shortcuts import get_object_or_404
import unittest


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
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        self.user_profile = UserProfile.objects.create(user=self.user)
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

        self.rating_data = {

            'user': self.user_profile,
            'position': self.movie1,
            'rating': 4
        }

    def test_movieshelf_rating_form_valid_data(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post('/scenario/result/tt1234567', {'website_ratings': 'True', 'rating': 4})
        self.assertEqual(response.status_code, 200)

        rating = MovieShelfRating.objects.filter(position='tt1234567').first()
        self.assertIsNotNone(rating)
        self.assertEqual(rating.rating, 4)

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


class PositionsWatchedByUserViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@email.com',
            password='secret2'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser3',
            email='test3@email.com',
            password='secret3'
        )

        self.movie1 = Movie.objects.create(Title='TestMovie3',
                                           Year='2024',
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
                                           imdbID='tt1234590',
                                           Type='movie',
                                           DVD='N/A',
                                           BoxOffice='21372137 $',
                                           Production='Pixel Studio 3',
                                           Website='https://www.pixelslifeisgreat.com',
                                           totalSeasons='',
                                           )

        self.movie2 = Movie.objects.create(Title='TestMovie4',
                                           Year='2024',
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
                                           imdbID='tt1234599',
                                           Type='movie',
                                           DVD='N/A',
                                           BoxOffice='21374102 $',
                                           Production='Pixel Studio 4',
                                           Website='https://www.pixelslifeisthebest.com',
                                           totalSeasons='',
                                           )

        self.user_profile = UserProfile.objects.create(user=self.user)
        self.watched_by_user = WatchedByUser.objects.create(user=self.user_profile)
        self.watched_by_user.watched.add(self.movie1)
        self.watched_by_user.watched.add(self.movie2)

        self.user_profile2 = UserProfile.objects.create(user=self.user2)
        self.watched_by_user2 = WatchedByUser.objects.create(user=self.user_profile2)

    def test_position_watched_by_user_view_returns_200(self):
        response = self.client.get(f'/scenario/users/{self.user.id}/watched')
        self.assertEqual(response.status_code, 200)

    def test_position_watched_by_user_view_returns_200_by_url_name(self):
        response = self.client.get(reverse('watched_by_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_position_watched_by_user_view_uses_correct_template(self):
        response = self.client.get(reverse('watched_by_user', args=[self.user.id]))
        self.assertTemplateUsed(response, 'watched_by_user.html')

    def test_position_watched_by_user_view_display_correct_positions(self):
        # self.client.login(username='testuser2', password='secret2')
        response = self.client.get(f'/scenario/users/{self.user.id}/watched')
        content = response.content.decode().replace(' ', '').replace('\n', '')
        self.assertRegex(content, f"{self.movie1.Title}.*{self.movie2.Title}")

    def test_position_watched_by_user_view_contains_correct_positions_number(self):
        # self.client.login(username='testuser2', password='secret2')
        response = self.client.get(f'/scenario/users/{self.user.id}/watched')
        self.assertEqual(response.context['watched_all'].count(), 2)

    def test_position_watched_by_user_view_no_watched_positions(self):
        # self.client.login(username='testuser3', password='secret3')
        response = self.client.get(f'/scenario/users/{self.user2.id}/watched')
        self.assertContains(response, 'No position watched yet')

    def test_position_watched_by_user_view_no_watched_positions_contains_correct_positions_number(self):
        response = self.client.get(f'/scenario/users/{self.user2.id}/watched')
        self.assertEqual(response.context['watched_all'].count(), 0)

    @unittest.expectedFailure
    def test_position_watched_by_user_invalid_user_id_returns_404(self):
        self.client.get('/scenario/users/169/watched')


class PositionsToWatchByUserViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username='testuser5',
            email='test2@email.com',
            password='secret6'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser6',
            email='test3@email.com',
            password='secret6'
        )

        self.movie3 = Movie.objects.create(Title='TestMovie5',
                                           Year='2025',
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
                                           imdbID='tt1234500',
                                           Type='movie',
                                           DVD='N/A',
                                           BoxOffice='21372137 $',
                                           Production='Pixel Studio 3',
                                           Website='https://www.pixelslifeisgreat.com',
                                           totalSeasons='',
                                           )

        self.movie4 = Movie.objects.create(Title='TestMovie6',
                                           Year='2026',
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
                                           imdbID='tt1234511',
                                           Type='movie',
                                           DVD='N/A',
                                           BoxOffice='21374102 $',
                                           Production='Pixel Studio 4',
                                           Website='https://www.pixelslifeisthebest.com',
                                           totalSeasons='',
                                           )

        self.user_profile = UserProfile.objects.create(user=self.user)
        self.to_watch_by_user = ToWatchByUser.objects.create(user=self.user_profile)
        self.to_watch_by_user.to_watch.add(self.movie3)
        self.to_watch_by_user.to_watch.add(self.movie4)

        self.user_profile2 = UserProfile.objects.create(user=self.user2)
        self.to_watch_by_user2 = ToWatchByUser.objects.create(user=self.user_profile2)

    def test_position_to_watch_by_user_view_returns_200(self):
        response = self.client.get(f'/scenario/users/{self.user.id}/to_watch')
        self.assertEqual(response.status_code, 200)

    def test_position_to_watch_by_user_view_returns_200_by_url_name(self):
        response = self.client.get(reverse('to_watch_by_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_position_to_watch_by_user_view_uses_correct_template(self):
        response = self.client.get(reverse('to_watch_by_user', args=[self.user.id]))
        self.assertTemplateUsed(response, 'to_watch_by_user.html')

    def test_position_to_watch_by_user_view_display_correct_positions(self):
        # self.client.login(username='testuser2', password='secret2')
        response = self.client.get(f'/scenario/users/{self.user.id}/to_watch')
        content = response.content.decode().replace(' ', '').replace('\n', '')
        self.assertRegex(content, f"{self.movie3.Title}.*{self.movie4.Title}")

    def test_position_to_watch_by_user_view_contains_correct_positions_number(self):
        # self.client.login(username='testuser2', password='secret2')
        response = self.client.get(f'/scenario/users/{self.user.id}/to_watch')
        self.assertEqual(response.context['to_watch_all'].count(), 2)

    def test_position_to_watch_by_user_view_no_watched_positions(self):
        # self.client.login(username='testuser3', password='secret3')
        response = self.client.get(f'/scenario/users/{self.user2.id}/to_watch')
        self.assertContains(response, 'No position to watch yet')

    def test_position_to_watch_by_user_view_no_watched_positions_contains_correct_positions_number(self):
        response = self.client.get(f'/scenario/users/{self.user2.id}/to_watch')
        self.assertEqual(response.context['to_watch_all'].count(), 0)

    @unittest.expectedFailure
    def test_position_to_watch_by_user_invalid_user_id_returns_404(self):
        self.client.get('/scenario/users/169/to_watch')
