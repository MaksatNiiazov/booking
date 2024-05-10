from rest_framework import serializers
from apps.property.models import Address, Amenity, Property, Room, PropertyPhoto, RoomPhotos, Review


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = ['uuid', 'photo']


class RoomPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPhotos
        fields = ['uuid', 'photo']


class RoomSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    photos = RoomPhotosSerializer(source='roomphotos_set', many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    photos = PropertyPhotoSerializer(source='propertyphoto_set', many=True, read_only=True)
    total_rooms = serializers.SerializerMethodField()
    free_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'
        
    def get_total_rooms(self, obj):
        return obj.hotel_rooms.count()

    def get_free_rooms(self, obj):
        return obj.hotel_rooms.filter(available=True).count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
        extra_kwargs = {
            'rooms': {'read_only': True},
            'amenities': {'read_only': True}
        }



