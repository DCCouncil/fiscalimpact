from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from app import views

from app.views import LatestEntriesFeed

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'legalsuff.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'app.views.home', name='home'),
    url(r'^rss/$', LatestEntriesFeed()),
    url(r'^view/$', 'app.views.view_documents', name='view_documents'),
    url(r'^view/(?P<pk>[\w|-]+)/$', 'app.views.print_documents', name='print_documents'),
    url(r'^published/$', 'app.views.published_query', name='published_query'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/$', 'app.views.search', name='search'),
    url(r'^document/$', 'app.views.new_document', name='new_document'),
    url(r'^document/(?P<pk>[\w|-]+)/$', login_required(views.DocumentUpdate.as_view()), name='document-detail'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'redirect_field_name':'/'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    url(r'^redactor/', include('redactor.urls')), 
)
