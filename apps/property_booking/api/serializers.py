from rest_framework import serializers
from apps.property_booking.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ['user', 'total_cost', 'status', 'procent', 'is_active']
