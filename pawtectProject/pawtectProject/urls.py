
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls import url,include
from pawtectProject  import settings
from django.views.static import serve
from pawtectApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^pawtectApp/',include('pawtectApp.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.ASSETS}),
]
