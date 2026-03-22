from core.tests import BaseTestCase
from movie.models import Movie
from rest_framework import status


class MovieAPITestCase(BaseTestCase):
    
    def test_list_movies_unauthenticated(self):
        url = '/api/movies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_movies_authenticated(self):
        self.authenticate_as_customer()
        url = '/api/movies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_movie_as_admin(self):
        self.authenticate_as_admin()
        url = '/api/movies/'
        data = {
            'title': 'New Movie',
            'description': 'New Description',
            'duration': 150,
            'release_date': '2025-06-01',
            'genre': 'comedy'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Movie')
    
    def test_create_movie_as_customer_denied(self):
        self.authenticate_as_customer()
        url = '/api/movies/'
        data = {
            'title': 'New Movie',
            'description': 'New Description',
            'duration': 150,
            'release_date': '2025-06-01',
            'genre': 'comedy'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_movie_detail(self):
        url = f'/api/movies/{self.movie.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Movie')
    
    def test_update_movie_as_admin(self):
        self.authenticate_as_admin()
        url = f'/api/movies/{self.movie.id}/'
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
    
    def test_delete_movie_as_admin(self):
        self.authenticate_as_admin()
        url = f'/api/movies/{self.movie.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        movie = Movie.objects.get(id=self.movie.id)
        self.assertFalse(movie.is_active)
    
    def test_filter_movies_by_genre(self):
        url = '/api/movies/?genre=action'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_movies(self):
        url = '/api/movies/?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
