from rest_framework import serializers
from .models import Payment
from booking.serializers import BookingListSerializer


class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingListSerializer(read_only=True)
    booking_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'booking', 'booking_id', 'amount', 'method', 'status', 
                  'transaction_id', 'payment_details', 'payment_date', 'updated_at']
        read_only_fields = ['id', 'status', 'transaction_id', 'payment_date', 'updated_at']


class PaymentCreateSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=Payment.PAYMENT_METHOD_CHOICES)
    payment_details = serializers.JSONField(required=False, default=dict)

    def validate_booking_id(self, value):
        from booking.models import Booking
        try:
            booking = Booking.objects.get(id=value, status='pending')
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Booking not found or not pending")
        return value


class PaymentListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='booking.id', read_only=True)
    movie_title = serializers.CharField(source='booking.show.movie.title', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'booking_id', 'movie_title', 'amount', 'method', 
                  'status', 'transaction_id', 'payment_date']
