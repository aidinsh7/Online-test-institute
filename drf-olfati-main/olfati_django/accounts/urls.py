from django.urls import path

from accounts.views import SendCode, VerifyOTPView, UserView

urlpatterns = [
    path("login", SendCode.as_view()),
    path("verify-otp", VerifyOTPView.as_view()),
    path("create-user", UserView.as_view())
]
