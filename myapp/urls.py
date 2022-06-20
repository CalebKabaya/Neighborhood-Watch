from django.urls import  re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    re_path('^$',views.index,name="index"),
    re_path('login/',views.signin,name='login'),
    re_path('register/',views.register,name='register'),
    re_path('signout/',views.signout,name='signout'),
    re_path('profile/',views.profile,name='profile'),
    re_path('update', views.update_profile, name='update'),
    re_path('new-hood/', views.posthood, name='newhood'),
    re_path('newpost/', views.addposts, name='newpost'),

    re_path('displayhood/', views.displayhood, name='displayhood'),
    re_path('displaypost/', views.displaypost, name='displaypost'),

    re_path(r'^joinhood/(?P<id>\d+)?$', views.join_hood, name='joinhood'), 
    re_path(r'^leavehood/(?P<id>\d+)?$', views.leave_hood, name='leavehood'), 
    re_path(r'^viewhood/(?P<hood_id>\d+)?$', views.viewhood, name='viewhood'), 
    # re_path(r'^addpost/(?P<hood_id>\d+)?$', views.add_post, name='addpost'), 

    # re_path(r'^newpost/(?P<hood_id>\d+)?$', views.add_post, name='newpost'),
    re_path(r'^addpost/$', views.new_post, name='addpost'),


    # re_path('newpost/<hood_id>', views.create_post, name='newpost'),
    # re_path(r'^newpost/(?P<hood_id>\d+)?$', views.addpost, name='newpost'), 

    # re_path('newpost/',views.create_post,name='newpost'),
    # re_path('add_post_comment/<int:post_id>',views.add_post_comment,name='add_post_comment'),

        # path('<hood_id>/members', views.hood_members, name='members'),
    # re_path('createpost/',views.create_post,name='createpost'),
    # re_path(r'^newpost$', views.new_post, name='newpost'),
    # re_path('newpost', views.create_post, name='newpost'),

    # re_path(r'^newpost/<int:hood_id>',views.add_post,name='newpost'),

    re_path(r'^members/(?P<hood_id>\d+)?$', views.hood_members, name='members'), 
    re_path('search/', views.search_business, name='search'),




 

  
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

  