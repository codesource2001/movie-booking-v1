from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from user.permissions import IsAdminUser, IsTheatreOwner
from .serializers import ShowSerializer, ShowListSerializer, ShowCreateSerializer
from .services import ShowService


class ShowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['start_time', 'price', 'created_at']
    ordering = ['start_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ShowService()

    def get_serializer_class(self):
        if self.action == 'create':
            return ShowCreateSerializer
        if self.action == 'list':
            return ShowListSerializer
        return ShowSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTheatreOwner()]
        return super().get_permissions()

    def get_queryset(self):
        is_admin = hasattr(self.request.user, 'is_admin') and self.request.user.is_admin
        
        movie_id = self.request.query_params.get('movie')
        if movie_id:
            return self.service.get_shows_by_movie(movie_id)
        
        screen_id = self.request.query_params.get('screen')
        if screen_id:
            return self.service.get_shows_by_screen(screen_id)
        
        date = self.request.query_params.get('date')
        if date:
            return self.service.get_shows_by_date(date)
        
        return self.service.get_all_shows(is_admin)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        show = self.service.create_show(serializer.validated_data)
        return Response(ShowSerializer(show).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        show = self.service.get_show_by_id(pk)
        
        if not show:
            return Response({'error': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(show, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        show = self.service.update_show(show, serializer.validated_data)
        return Response(ShowSerializer(show).data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        show = self.service.get_show_by_id(pk)
        
        if not show:
            return Response({'error': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)
        
        self.service.delete_show(show)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        show = self.service.get_show_by_id(pk)
        if not show:
            return Response({'error': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(self.service.get_available_seats(show))

    @action(detail=False, methods=['get'], url_path='by-movie/(?P<movie_id>[^/.]+)')
    def by_movie(self, request, movie_id=None):
        shows = self.service.get_shows_by_movie(movie_id)
        serializer = ShowListSerializer(shows, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-theatre/(?P<theatre_id>[^/.]+)')
    def by_theatre(self, request, theatre_id=None):
        shows = self.service.get_shows_by_theatre(theatre_id)
        serializer = ShowListSerializer(shows, many=True)
        return Response(serializer.data)
