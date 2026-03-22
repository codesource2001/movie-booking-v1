from rest_framework import serializers
from .models import Theatre, Screen


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['id', 'name', 'screen_type', 'total_seats', 'seats_layout']
        read_only_fields = ['id']


class TheatreSerializer(serializers.ModelSerializer):
    screens = ScreenSerializer(many=True, read_only=True)
    
    class Meta:
        model = Theatre
        fields = ['id', 'name', 'location', 'address', 'total_seats', 'seats_layout', 
                  'facilities', 'is_active', 'screens', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TheatreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = ['id', 'name', 'location', 'total_seats', 'is_active']
