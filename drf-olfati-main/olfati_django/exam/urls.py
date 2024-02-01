from django.urls import path

from .views import ExamListView, ExamView, ExamKarNameView, ListCreateMyClassView

urlpatterns = [
    path('class-list/', ListCreateMyClassView.as_view({'get': 'list'})),
    path('class-list/<int:pk>/', ListCreateMyClassView.as_view({'get': 'retrieve'})),
    path("list", ExamListView.as_view()),
    path("list/<int:pk>/", ExamListView.as_view()),
    path("<int:pk>", ExamView.as_view()),
    path("", ExamView.as_view()),
    path("kar-name", ExamKarNameView.as_view()),
   

]
