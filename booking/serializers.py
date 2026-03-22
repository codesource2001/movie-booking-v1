from rest_framework import serializers
from .models import Booking
from show.serializers import ShowListSerializer
from user.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    show = ShowListSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    show_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'show', 'seats', 'total_price', 'status', 
                  'booking_date', 'updated_at', 'show_id']
        read_only_fields = ['id', 'user', 'total_price', 'status', 
                           'booking_date', 'updated_at']


class BookingCreateSerializer(serializers.Serializer):
    show_id = serializers.IntegerField()
    seats = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        help_text="List of seat numbers like ['A1', 'A2', 'B1']"
    )

    def validate_show_id(self, value):
        from show.models import Show
        try:
            show = Show.objects.get(id=value, status__in=['scheduled', 'running'])
        except Show.DoesNotExist:
            raise serializers.ValidationError("Show not found or not available")
        return value

    def validate(self, data):
        from show.models import Show
        show = Show.objects.get(id=data['show_id'])
        seats = data['seats']
        
        if len(seats) > show.available_seats:
            raise serializers.ValidationError("Not enough available seats")
        
        return data


class BookingListSerializer(serializers.ModelSerializer):
    show_title = serializers.CharField(source='show.movie.title', read_only=True)
    show_time = serializers.CharField(source='show.start_time', read_only=True)
    theatre_name = serializers.CharField(source='show.screen.theatre.name', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'show_title', 'show_time', 'theatre_name', 'seats', 
                  'total_price', 'status', 'booking_date']
