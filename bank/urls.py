from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_page, name = "login_page"),
    path('<int:acct_no>/',views.acct_details, name= "acct_details"),
    path('<int:acct_no>/statement/',views.acct_statement, name = "acct_statement")
]