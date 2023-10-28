from django.urls import path

from litner.views import LitnerListView, LitnerView

urlpatterns = [
    path("list", LitnerListView.as_view()),
    path("<int:pk>", LitnerListView.as_view()),
    path("list/<int:pk>/", LitnerListView.as_view()),
    path("", LitnerView.as_view()),
   # path("kar-name/", LitnerKarNameView.as_view())

]
