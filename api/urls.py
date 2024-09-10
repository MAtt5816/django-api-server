from django.urls import path
from .views import HelloWorldView, AuthorizeView, StudentListView, StudentDetailView

urlpatterns = [
    path('hello', HelloWorldView.as_view(), name='hello_world'),
    path('authorize', AuthorizeView.as_view(), name='authorize'),
    path('student', StudentListView.as_view(), name='student_list'),
    path('student/<int:studentId>', StudentDetailView.as_view(), name='student_detail'),
]
