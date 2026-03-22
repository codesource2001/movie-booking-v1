from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from user.permissions import IsAdminUser, IsAdminOrReadOnly
from .serializers import MovieSerializer, MovieListSerializer
from .services import MovieService


class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'genre']
    ordering_fields = ['release_date', 'created_at', 'title']
    ordering = ['-release_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = MovieService()

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieSerializer

    def get_queryset(self):
        is_admin = hasattr(self.request.user, 'is_admin') and self.request.user.is_admin
        
        genre = self.request.query_params.get('genre')
        if genre:
            return self.service.get_movies_by_genre(genre)
        
        return self.service.get_all_movies(is_admin)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        is_admin = hasattr(request.user, 'is_admin') and request.user.is_admin
        movie = self.service.get_movie_by_id(pk, is_admin)
        
        if not movie:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(movie)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = self.service.create_movie(serializer.validated_data)
        return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        movie = self.service.get_movie_by_id(pk, is_admin=True)
        
        if not movie:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(movie, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        movie = self.service.update_movie(movie, serializer.validated_data)
        return Response(MovieSerializer(movie).data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        movie = self.service.get_movie_by_id(pk, is_admin=True)
        
        if not movie:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        self.service.delete_movie(movie)
        return Response(status=status.HTTP_204_NO_CONTENT)
