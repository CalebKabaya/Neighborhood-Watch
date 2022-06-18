from django.urls import  re_path
from . import views

urlpatterns=[
    re_path('^$',views.index,name="index"),
    re_path('login/',views.signin,name='login'),
    re_path('register/',views.register,name='register'),
    re_path('signout/',views.signout,name='signout'),
    
]
  