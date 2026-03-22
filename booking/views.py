from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from user.permissions import IsOwnerOrAdmin
from .serializers import BookingSerializer, BookingCreateSerializer, BookingListSerializer
from .services import BookingService


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['booking_date', 'total_price', 'status']
    ordering = ['-booking_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = BookingService()

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        if self.action == 'list':
            return BookingListSerializer
        return BookingSerializer

    def get_queryset(self):
        is_admin = hasattr(self.request.user, 'is_admin') and self.request.user.is_admin
        return self.service.get_user_bookings(self.request.user, is_admin)

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        booking, error = self.service.create_booking(
            user=request.user,
            show_id=serializer.validated_data['show_id'],
            seats=serializer.validated_data['seats']
        )
        
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_booking(self, request, pk=None):
        booking = self.service.get_booking_by_id(pk, request.user, request.user.is_admin)
        
        if not booking:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        
        booking, error = self.service.cancel_booking(booking, request.user, request.user.is_admin)
        
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(BookingSerializer(booking).data)

    @action(detail=False, methods=['get'], url_path='my-bookings')
    def my_bookings(self, request):
        bookings = self.service.get_user_bookings(request.user)
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request):
        status_filter = request.query_params.get('status')
        bookings = self.service.get_booking_history(request.user, status_filter)
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
