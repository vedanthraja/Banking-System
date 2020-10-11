from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.create,name='create'),
    path(r'<str:pan>',views.pinnumber,name='pin_number'),
    path('login/',views.login_page, name = "login_page"),
    path('<int:acct_no>/',views.acct_details, name= "acct_details"),
    path('<int:acct_no>/statement/',views.acct_statement, name = "acct_statement"),
    path('add/',views.cust_add_acct, name = "cust_add_acct"),
]