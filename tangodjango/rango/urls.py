from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^edit_profile/$', views.edit_profile, name='edit_profile'), 
        url(r'^goto/', views.track_url, name ='goto'),
        url(r'^add_profile/', views.register_profile, name ="register_profile"),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^profile/(?P<user_name>[\w\-]+)/', views.user_profile, name='user_profile'),
        url(r'^users/', views.all_users, name ='all_users'),
              
        )
