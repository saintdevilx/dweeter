from django.conf.urls import url, include
from .views import *
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
	url(r'^$',home, name='home'),
	url(r'^u/(?P<username>[a-zA-Z0-9_]+)$',view_profile, name='view_profile'),	
	url(r'^(?P<username>[a-zA-Z0-9_]+)/dweets$',user_dweet, name='user_dweet'),	
	url(r'^login$',login, name='login'),	
	url(r'^logout$',logout, name='logout'),	
	url(r"^add_new_dweet$", add_new_dweet, name='add_new_dweet'),
	url(r"^people_list$", people_list, name='people_list'),
	url(r"^follow$", follow_user, name='follow_user'),
	url(r"^like$", add_like, name='add_like'),
	url(r"^add_reply$", add_reply, name='add_reply'),
	url(r"^dweet_list$", dweet_list, name='dweet_list'),
	url(r"^(?P<dweet_id>[0-9]+)/dweet_reply$",dweet_list, name='dweet_reply_list'),
	url(r"^search/(?P<category>[a-zA-Z]+)",search, name="search"),
	url(r'^register$',register, name='register'),
]