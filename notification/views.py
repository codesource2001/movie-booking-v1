from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from user.permissions import IsAdminUser
from .serializers import NotificationSerializer, NotificationListSerializer
from .services import NotificationService


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'is_read']
    ordering = ['-created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = NotificationService()

    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        return NotificationSerializer

    def get_queryset(self):
        is_admin = hasattr(self.request.user, 'is_admin') and self.request.user.is_admin
        return self.service.get_user_notifications(self.request.user, is_admin)

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.service.get_notification_by_id(pk, request.user, request.user.is_admin)
        
        if not notification:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        
        notification, error = self.service.mark_as_read(notification, request.user, request.user.is_admin)
        
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(NotificationSerializer(notification).data)

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        self.service.mark_all_as_read(request.user)
        return Response({'message': 'All notifications marked as read'})

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        is_admin = hasattr(request.user, 'is_admin') and request.user.is_admin
        count = self.service.get_unread_count(request.user, is_admin)
        return Response({'unread_count': count})

    @action(detail=False, methods=['get'], url_path='my-notifications')
    def my_notifications(self, request):
        notifications = self.service.get_user_notifications(request.user)
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data)
