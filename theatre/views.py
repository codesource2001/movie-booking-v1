from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from user.permissions import IsAdminUser, IsTheatreOwner
from .serializers import TheatreSerializer, TheatreListSerializer, ScreenSerializer
from .services import TheatreService


class TheatreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = TheatreService()

    def get_serializer_class(self):
        if self.action == 'list':
            return TheatreListSerializer
        return TheatreSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsTheatreOwner()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsTheatreOwner()]
        return super().get_permissions()

    def get_queryset(self):
        is_admin = hasattr(self.request.user, 'is_admin') and self.request.user.is_admin
        
        location = self.request.query_params.get('location')
        if location:
            return self.service.get_theatres_by_location(location)
        
        return self.service.get_all_theatres(is_admin)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        owner = None if request.user.is_admin else request.user
        theatre = self.service.create_theatre(serializer.validated_data, owner)
        
        return Response(TheatreSerializer(theatre).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        theatre = self.service.get_theatre_by_id(pk, is_admin=True)
        
        if not theatre:
            return Response({'error': 'Theatre not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_admin and theatre.owner != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(theatre, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        theatre = self.service.update_theatre(theatre, serializer.validated_data)
        return Response(TheatreSerializer(theatre).data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        theatre = self.service.get_theatre_by_id(pk, is_admin=True)
        
        if not theatre:
            return Response({'error': 'Theatre not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_admin and theatre.owner != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        self.service.delete_theatre(theatre)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def screens(self, request, pk=None):
        theatre = self.service.get_theatre_by_id(pk, is_admin=True)
        if not theatre:
            return Response({'error': 'Theatre not found'}, status=status.HTTP_404_NOT_FOUND)
        
        screens = self.service.get_screens_for_theatre(theatre)
        serializer = ScreenSerializer(screens, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsTheatreOwner])
    def add_screen(self, request, pk=None):
        theatre = self.service.get_theatre_by_id(pk, is_admin=True)
        if not theatre:
            return Response({'error': 'Theatre not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_admin and theatre.owner != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ScreenSerializer(data=request.data)
        if serializer.is_valid():
            screen = self.service.create_screen(theatre, serializer.validated_data)
            return Response(ScreenSerializer(screen).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
