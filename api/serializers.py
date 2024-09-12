from datetime import datetime

from rest_framework import serializers
from .models import Student, Location, Picture

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ['student']

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        exclude = ['student']

class StudentSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    picture = PictureSerializer()

    registered = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        picture_data = validated_data.pop('picture')

        validated_data['registered'] = datetime.now()
        student = Student.objects.create(**validated_data)

        Location.objects.create(student=student, **location_data)
        Picture.objects.create(student=student, **picture_data)

        return student

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        picture_data = validated_data.pop('picture', None)

        instance.gender = validated_data.get('gender', instance.gender)
        instance.title = validated_data.get('title', instance.title)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.registered = validated_data.get('registered', instance.registered)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.id_name = validated_data.get('id_name', instance.id_name)
        instance.id_value = validated_data.get('id_value', instance.id_value)
        instance.nat = validated_data.get('nat', instance.nat)

        if location_data:
            Location.objects.filter(student=instance).update(**location_data)

        if picture_data:
            Picture.objects.filter(student=instance).update(**picture_data)

        instance.save()

        return instance

class AuthDataSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    passphrase = serializers.CharField(max_length=255)

class HelloWorldSerializer(serializers.Serializer):
    message = serializers.CharField(default="Hello World!")

class JwtTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
