from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from user.permissions import IsAdminUser, IsOwnerOrAdmin
from .serializers import PaymentSerializer, PaymentCreateSerializer, PaymentListSerializer
from .services import PaymentService


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['payment_date', 'amount', 'status']
    ordering = ['-payment_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = PaymentService()

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        if self.action == 'list':
            return PaymentListSerializer
        return PaymentSerializer

    def get_queryset(self):
        is_admin = hasattr(self.request.user, 'is_admin') and self.request.user.is_admin
        return self.service.get_user_payments(self.request.user, is_admin)

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        if self.action == 'refund':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment, error = self.service.process_payment(
            user=request.user,
            booking_id=serializer.validated_data['booking_id'],
            method=serializer.validated_data['method'],
            payment_details=serializer.validated_data.get('payment_details')
        )
        
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='refund')
    def refund(self, request, pk=None):
        payment, error = self.service.process_refund(pk, is_admin=True)
        
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(PaymentSerializer(payment).data)

    @action(detail=False, methods=['get'], url_path='my-payments')
    def my_payments(self, request):
        payments = self.service.get_user_payments(request.user)
        serializer = PaymentListSerializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='booking/(?P<booking_id>[^/.]+)')
    def by_booking(self, request, booking_id=None):
        is_admin = hasattr(request.user, 'is_admin') and request.user.is_admin
        payments = self.service.get_user_payments(request.user, is_admin)
        payments = payments.filter(booking_id=booking_id)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
