from django.urls import path
from markethub.views import MarketHubListView, MarketHubView, QuestionView,MarketHubSearchView,UserAddMarkethub

urlpatterns = [
#class Markethub
    path("list", MarketHubListView.as_view()),
    path("<int:pk>", MarketHubListView.as_view()),
    path("list/<int:pk>", MarketHubListView.as_view()),
    path('MarketHubQuestionPaid/<int:pk>',MarketHubListView.as_view()),
    path('update/<int:pk>', MarketHubView.as_view()),
    path('delete/<int:pk>', MarketHubView.as_view()),
    path('detail/<int:pk>',MarketHubView.as_view()),
    path('search/',MarketHubSearchView.as_view()),
    path('paid_users/<int:pk>', QuestionView.as_view()),
]
