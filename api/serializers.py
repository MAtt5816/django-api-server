from rest_framework import serializers
from .models import Student, Location, Picture

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    picture = PictureSerializer()

    class Meta:
        model = Student
        fields = '__all__'

class AuthDataSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    passphrase = serializers.CharField(max_length=255)

class HelloWorldSerializer(serializers.Serializer):
    message = serializers.CharField(default="Hello World!")

class JwtTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
