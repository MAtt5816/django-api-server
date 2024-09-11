from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, User
from .serializers import StudentSerializer, AuthDataSerializer, HelloWorldSerializer, JwtTokenSerializer
import hashlib


class HelloWorldView(APIView):
    def get(self, request):
        data = "Hello World!"
        return Response(data, status=status.HTTP_200_OK, content_type='text/plain')


class AuthorizeView(APIView):
    def post(self, request):
        serializer = AuthDataSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.data['username']).exists():
                user = User.objects.get(username=serializer.data['username'])
            else:
                user = None

            if user is None:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            hash = hashlib.sha256((serializer.data['passphrase'] + user.salt).encode('UTF8'))
            if user.sha256 != hash.hexdigest():
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response(token, status=status.HTTP_200_OK, content_type='text/plain')
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class StudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = request.query_params.get('results', 1)
        try:
            results = int(results)
        except ValueError:
            return Response({"error": "Invalid 'results' parameter"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        students = Student.objects.all()[:results]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')

    def post(self, request):
        serializer = StudentSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, studentId):
        try:
            student = Student.objects.get(id=studentId)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    def patch(self, request, studentId):
        try:
            student = Student.objects.get(id=studentId)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    def delete(self, request, studentId):
        try:
            student = Student.objects.get(id=studentId)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
