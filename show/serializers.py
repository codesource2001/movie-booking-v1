from rest_framework import serializers
from .models import Show
from movie.serializers import MovieListSerializer
from theatre.serializers import ScreenSerializer


class ShowSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    screen = ScreenSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)
    screen_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Show
        fields = ['id', 'movie', 'screen', 'start_time', 'end_time', 'price', 
                  'available_seats', 'status', 'movie_id', 'screen_id', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'available_seats', 'status', 'created_at', 'updated_at']


class ShowListSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    screen_name = serializers.CharField(source='screen.name', read_only=True)
    theatre_name = serializers.CharField(source='screen.theatre.name', read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'movie_title', 'screen_name', 'theatre_name', 'start_time', 
                  'end_time', 'price', 'available_seats', 'status']


class ShowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'movie', 'screen', 'start_time', 'end_time', 'price', 'available_seats']
        read_only_fields = ['id', 'available_seats']

    def create(self, validated_data):
        movie = validated_data['movie']
        screen = validated_data['screen']
        validated_data['available_seats'] = screen.total_seats
        return super().create(validated_data)
