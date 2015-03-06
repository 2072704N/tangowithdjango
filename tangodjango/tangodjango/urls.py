from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from django.contrib.auth import views 

class MyRegistrationView(RegistrationView):
    def get_success_url(selfself,request,user):
        return '/rango/add_profile'
    
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tangodjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(),name = 'registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    #override registration urls
    url(r'^password/change/$',
                views.password_change,
                name='password_change'),
    #bit hacky but redirects user to rango once password change is done
    url(r'^rango/$',
                views.password_change_done,
                name='password_change_done'),
)

if settings.DEBUG:
    urlpatterns += patterns( 'django.views.static',(r'^media/(?P<path>.*)',
                                                    'serve', {'document_root':
                                                              settings.MEDIA_ROOT}),)
