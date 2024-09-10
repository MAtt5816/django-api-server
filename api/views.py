from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student
from .serializers import StudentSerializer, AuthDataSerializer, HelloWorldSerializer, JwtTokenSerializer


class HelloWorldView(APIView):
    def get(self, request):
        data = {"message": "Hello World!"}
        return Response(data, status=status.HTTP_200_OK)


class AuthorizeView(APIView):
    def post(self, request):
        serializer = AuthDataSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: Przykładowe tokeny, należy dodać własną autoryzację
            refresh = RefreshToken.for_user(request.user)
            return Response({"token": str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class StudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = request.query_params.get('results', 1)
        try:
            results = int(results)
        except ValueError:
            return Response({"error": "Invalid 'results' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        students = Student.objects.all()[:results]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, studentId):
        try:
            student = Student.objects.get(id=studentId)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, studentId):
        try:
            student = Student.objects.get(id=studentId)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
